#!/usr/bin/env python3
"""
cost_guard.py — Phase 3i godspeed cost / efficiency guard.

Maps Brain severity tiers (S0-S5) to USD budget ceilings, gates live agent
invocations so unbounded iter loops can't quietly burn $5+, and writes
post-flight efficiency receipts to ~/.claude/telemetry/brain/cost_efficiency.jsonl.

Three concerns:
1. Pre-flight: route_full stamps budget_usd + tier on the dispatch envelope so
   the caller sees the cost contract before invocation.
2. Mid-flight: invoke_live calls is_breach(running_cost, budget_usd) after each
   tool-use iteration; on breach it aborts with verdict=BUDGET_EXCEEDED.
3. Post-flight: invoke() builds a CostReceipt and appends it to the JSONL log
   for downstream rollups (aurora, dashboard, learnings ROI).

Sacred Rule alignment:
- Rule 1 (truthful): caps based on actual measured cost, no estimation drift
- Rule 2 (non-destructive): receipts append-only, never delete telemetry
- Rule 4 (only-asked): does NOT auto-escalate or auto-downgrade tier;
  surfaces BUDGET_EXCEEDED and lets caller decide whether to retry on a
  bigger budget or downgrade to a cheaper agent
- Rule 9 (no options): single canonical budget table, deterministic gate
- Rule 11 (AAA): every receipt row reproducible — same input yields same row
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Budget table: Brain tier → USD ceiling per agent invocation.
# Calibrated against LIVE Sonnet receipts 2026-05-02..03 in agent_invocations.jsonl:
#   urania $0.0190 (no tools), $0.0274 (PASS w/ tools), $0.0571 (Windows shell bug),
#   $0.1169 (max_iter cap hit at 8) — S3 ceiling at $0.50 covers worst-case 4×.
# Opus budgets sized for extended-thinking + multi-step blueprints (S4-S5).
TIER_BUDGETS_USD = {
    "S0": 0.005,   # trivial chit-chat / status check (Haiku-class)
    "S1": 0.020,   # quick lookup / single tool call (Haiku-class)
    "S2": 0.100,   # Sonnet research-agent call (urania $0.0274 verified)
    "S3": 0.500,   # Sonnet multi-iteration tool loop
    "S4": 2.000,   # Opus extended-thinking architecture work
    "S5": 5.000,   # Opus deep-synthesis multi-step blueprint
}

# Soft-cap multiplier — invocations abort when running cost crosses this
# fraction of budget. 1.5× lets normal variance through but catches runaway
# tool loops (e.g. agent stuck calling bash 12× at $0.05/iter on Sonnet).
BUDGET_BREACH_MULTIPLIER = 1.5

# Default tier inference from agent model when caller doesn't pass tier explicitly.
MODEL_TO_TIER_DEFAULT = {
    "haiku":  "S1",
    "sonnet": "S2",
    "opus":   "S4",
}

RECEIPT_PATH = Path.home() / ".claude" / "telemetry" / "brain" / "cost_efficiency.jsonl"


def budget_for_tier(tier: str | None) -> float:
    """Return USD budget ceiling for a Brain tier; defaults to S2 if unknown/None."""
    if not tier:
        return TIER_BUDGETS_USD["S2"]
    return TIER_BUDGETS_USD.get(tier.upper(), TIER_BUDGETS_USD["S2"])


def tier_for_model(model: str | None) -> str:
    """Best-effort tier when no Brain/Director tier is supplied."""
    if not model:
        return "S2"
    return MODEL_TO_TIER_DEFAULT.get(model.lower(), "S2")


def is_breach(running_cost_usd: float, budget_usd: float) -> bool:
    """Return True if running cost has crossed the breach threshold.

    Threshold is rounded to 6 decimals so e.g. 0.15 clearly meets the
    1.5× S2 boundary instead of getting clipped by float multiplication
    drift (0.1 * 1.5 == 0.15000000000000002 in IEEE-754).
    """
    if budget_usd <= 0:
        return False
    threshold = round(budget_usd * BUDGET_BREACH_MULTIPLIER, 6)
    return running_cost_usd >= threshold


@dataclass
class CostReceipt:
    """One post-flight cost-efficiency receipt."""
    ts: str
    session_id: str
    agent: str
    tier: str
    budget_usd: float
    actual_cost_usd: float
    iterations: int
    cache_hit_rate: Optional[float]
    verdict: str
    breach: bool
    efficiency_ratio: float  # actual / budget — < 1.0 = under, ≥ 1.5 = breach
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "ts": self.ts,
            "session_id": self.session_id,
            "agent": self.agent,
            "tier": self.tier,
            "budget_usd": round(self.budget_usd, 6),
            "actual_cost_usd": round(self.actual_cost_usd, 6),
            "iterations": self.iterations,
            "cache_hit_rate": (
                round(self.cache_hit_rate, 4) if self.cache_hit_rate is not None else None
            ),
            "verdict": self.verdict,
            "breach": self.breach,
            "efficiency_ratio": round(self.efficiency_ratio, 4),
            "notes": self.notes,
        }


def build_receipt(
    *,
    agent: str,
    tier: str,
    actual_cost_usd: float,
    iterations: int,
    cache_hit_rate: Optional[float] = None,
    verdict: str = "UNKNOWN",
    session_id: Optional[str] = None,
    notes: Optional[list[str]] = None,
) -> CostReceipt:
    """Build a CostReceipt with computed fields filled in."""
    budget = budget_for_tier(tier)
    breach = is_breach(actual_cost_usd, budget)
    ratio = (actual_cost_usd / budget) if budget > 0 else 0.0
    return CostReceipt(
        ts=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        session_id=session_id or os.environ.get("CLAUDE_SESSION_ID", ""),
        agent=agent,
        tier=tier,
        budget_usd=budget,
        actual_cost_usd=actual_cost_usd,
        iterations=iterations,
        cache_hit_rate=cache_hit_rate,
        verdict=verdict,
        breach=breach,
        efficiency_ratio=ratio,
        notes=list(notes or []),
    )


def write_receipt(receipt: CostReceipt) -> bool:
    """Append one receipt row. Non-blocking — returns False on any failure."""
    try:
        RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RECEIPT_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(receipt.to_dict(), ensure_ascii=False) + "\n")
        return True
    except Exception:
        return False


def load_receipts(limit: int = 0) -> list[dict]:
    """Read receipts (newest first if limit>0). Returns empty list on missing file."""
    if not RECEIPT_PATH.exists():
        return []
    with open(RECEIPT_PATH, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    if limit > 0:
        rows = rows[-limit:]
    return rows


def rollup_efficiency(rows: Optional[list[dict]] = None) -> dict:
    """Aggregate receipts into a summary: total spend, breach rate, avg efficiency."""
    rows = rows if rows is not None else load_receipts()
    if not rows:
        return {
            "receipt_count": 0,
            "total_actual_usd": 0.0,
            "total_budget_usd": 0.0,
            "breach_count": 0,
            "breach_rate": 0.0,
            "avg_efficiency_ratio": 0.0,
            "by_agent": {},
            "by_tier": {},
        }
    total_actual = sum(r.get("actual_cost_usd", 0.0) for r in rows)
    total_budget = sum(r.get("budget_usd", 0.0) for r in rows)
    breach_count = sum(1 for r in rows if r.get("breach"))
    avg_ratio = sum(r.get("efficiency_ratio", 0.0) for r in rows) / len(rows)

    by_agent: dict[str, dict] = {}
    by_tier: dict[str, dict] = {}
    for r in rows:
        agent = r.get("agent", "?")
        tier = r.get("tier", "?")
        for bucket, key in ((by_agent, agent), (by_tier, tier)):
            entry = bucket.setdefault(key, {
                "fires": 0, "actual_usd": 0.0, "budget_usd": 0.0, "breaches": 0,
            })
            entry["fires"] += 1
            entry["actual_usd"] += r.get("actual_cost_usd", 0.0)
            entry["budget_usd"] += r.get("budget_usd", 0.0)
            if r.get("breach"):
                entry["breaches"] += 1

    for entry in (*by_agent.values(), *by_tier.values()):
        entry["actual_usd"] = round(entry["actual_usd"], 6)
        entry["budget_usd"] = round(entry["budget_usd"], 6)

    return {
        "receipt_count": len(rows),
        "total_actual_usd": round(total_actual, 6),
        "total_budget_usd": round(total_budget, 6),
        "breach_count": breach_count,
        "breach_rate": round(breach_count / len(rows), 4),
        "avg_efficiency_ratio": round(avg_ratio, 4),
        "by_agent": by_agent,
        "by_tier": by_tier,
    }


def cache_hit_rate(input_tokens: int, cache_read_tokens: int, cache_creation_tokens: int) -> Optional[float]:
    """Same definition as agent_runner.telemetry_rollup — kept here so cost_guard
    is standalone without importing back into agent_runner (avoid circular import).
    """
    denom = input_tokens + cache_read_tokens + cache_creation_tokens
    if denom <= 0:
        return None
    return cache_read_tokens / denom


# ---------------------------------------------------------------------------
# Pricing — USD per million tokens for the Claude 4.x family (2026-current).
# Used by audit_transcript to estimate would-be cost for any historical session.
# Update if Anthropic changes pricing — these are reproducible from
# https://www.anthropic.com/pricing.
# ---------------------------------------------------------------------------
PRICING_USD_PER_MTOK = {
    "haiku":  {"input": 1.00,  "output":  5.00, "cache_read": 0.10,  "cache_write": 1.25},
    "sonnet": {"input": 3.00,  "output": 15.00, "cache_read": 0.30,  "cache_write": 3.75},
    "opus":   {"input": 15.00, "output": 75.00, "cache_read": 1.50,  "cache_write": 18.75},
}


def _model_family(model: str | None) -> str:
    """Return haiku/sonnet/opus from a verbose model id like 'claude-sonnet-4-7'."""
    if not model:
        return "sonnet"
    m = model.lower()
    for fam in ("haiku", "sonnet", "opus"):
        if fam in m:
            return fam
    return "sonnet"


def compute_cost_from_usage(
    *,
    model: str | None,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cache_read_tokens: int = 0,
    cache_creation_tokens: int = 0,
) -> float:
    """Compute USD cost for one Anthropic API call from a usage block.

    Maps `model` to a family (haiku/sonnet/opus), then applies per-token-class
    pricing. Returns 0.0 for unknown families (falls through to sonnet defaults).
    """
    fam = _model_family(model)
    rates = PRICING_USD_PER_MTOK.get(fam, PRICING_USD_PER_MTOK["sonnet"])
    cost = (
        (input_tokens          * rates["input"]      / 1_000_000)
        + (output_tokens         * rates["output"]     / 1_000_000)
        + (cache_read_tokens     * rates["cache_read"] / 1_000_000)
        + (cache_creation_tokens * rates["cache_write"] / 1_000_000)
    )
    return round(cost, 6)


def audit_transcript(transcript_path: str | Path) -> dict:
    """Audit any Claude Code transcript JSONL for cost + would-be breach analysis.

    Reads each `assistant` message's usage block, computes cost using
    compute_cost_from_usage, infers the tier from the message's model field,
    and flags rows that would have tripped the per-tier soft-cap.

    Returns a summary dict:
      - row_count
      - total_cost_usd
      - by_model: per-family aggregates
      - would_breach_count: how many messages would have breached a tier ceiling
      - top_message_costs: 5 most expensive single messages with model + tokens
      - errors: list of parse failures (file may be partial)
    """
    path = Path(transcript_path)
    if not path.exists():
        return {"error": f"transcript not found: {path}", "row_count": 0}

    by_model: dict[str, dict] = {}
    msg_costs: list[dict] = []
    total = 0.0
    errors: list[str] = []
    would_breach = 0

    with open(path, encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"line {i}: {e}")
                continue
            msg = obj.get("message") or {}
            usage = msg.get("usage") or {}
            if not usage:
                continue
            model = msg.get("model") or obj.get("model") or "sonnet"
            cost = compute_cost_from_usage(
                model=model,
                input_tokens=int(usage.get("input_tokens") or 0),
                output_tokens=int(usage.get("output_tokens") or 0),
                cache_read_tokens=int(usage.get("cache_read_input_tokens") or 0),
                cache_creation_tokens=int(usage.get("cache_creation_input_tokens") or 0),
            )
            total += cost
            fam = _model_family(model)
            entry = by_model.setdefault(fam, {"calls": 0, "cost_usd": 0.0})
            entry["calls"] += 1
            entry["cost_usd"] += cost
            tier = tier_for_model(fam)
            budget = budget_for_tier(tier)
            breach = is_breach(cost, budget)
            if breach:
                would_breach += 1
            msg_costs.append({
                "line": i, "model": fam, "tier": tier,
                "cost_usd": round(cost, 6), "budget_usd": budget,
                "would_breach": breach,
            })

    for entry in by_model.values():
        entry["cost_usd"] = round(entry["cost_usd"], 6)

    msg_costs.sort(key=lambda r: r["cost_usd"], reverse=True)
    return {
        "transcript": str(path),
        "row_count": len(msg_costs),
        "total_cost_usd": round(total, 6),
        "by_model": by_model,
        "would_breach_count": would_breach,
        "would_breach_rate": round(would_breach / len(msg_costs), 4) if msg_costs else 0.0,
        "top_message_costs": msg_costs[:5],
        "errors": errors[:10],
    }


def top_spenders(by: str = "agent", n: int = 10, rows: Optional[list[dict]] = None) -> list[dict]:
    """Return top-N spender entries by `agent` or `tier` from cost_efficiency receipts."""
    if by not in {"agent", "tier"}:
        raise ValueError(f"top_spenders.by must be 'agent' or 'tier', got {by!r}")
    rows = rows if rows is not None else load_receipts()
    if not rows:
        return []
    bucket: dict[str, dict] = {}
    for r in rows:
        key = r.get(by, "?")
        entry = bucket.setdefault(key, {
            by: key, "fires": 0, "actual_usd": 0.0, "budget_usd": 0.0, "breaches": 0,
        })
        entry["fires"] += 1
        entry["actual_usd"] += r.get("actual_cost_usd", 0.0)
        entry["budget_usd"] += r.get("budget_usd", 0.0)
        if r.get("breach"):
            entry["breaches"] += 1
    out = sorted(bucket.values(), key=lambda e: e["actual_usd"], reverse=True)
    for entry in out:
        entry["actual_usd"] = round(entry["actual_usd"], 6)
        entry["budget_usd"] = round(entry["budget_usd"], 6)
    return out[:n]


def breach_rows(rows: Optional[list[dict]] = None) -> list[dict]:
    """Return only the receipts where breach=True (tier ceiling tripped)."""
    rows = rows if rows is not None else load_receipts()
    return [r for r in rows if r.get("breach")]


def receipts_since(iso_date: str, rows: Optional[list[dict]] = None) -> list[dict]:
    """Filter receipts to those with ts >= iso_date (e.g. '2026-05-01')."""
    rows = rows if rows is not None else load_receipts()
    return [r for r in rows if (r.get("ts") or "") >= iso_date]


# CLI for ad-hoc inspection.
def _main(argv: list[str]) -> int:
    import argparse
    p = argparse.ArgumentParser(prog="cost_guard")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("budgets", help="Print the tier→USD budget table")
    sub.add_parser("rollup", help="Aggregate cost_efficiency.jsonl receipts")
    pr = sub.add_parser("recent", help="Show most-recent N receipts")
    pr.add_argument("--n", type=int, default=10)

    pa = sub.add_parser("audit", help="Audit any Claude Code transcript JSONL — would-be cost + breach report")
    pa.add_argument("transcript", help="Path to transcript JSONL (~/.claude/projects/<proj>/<session>.jsonl)")

    pt = sub.add_parser("top", help="Top spenders by agent or tier from receipts")
    pt.add_argument("--by", choices=["agent", "tier"], default="agent")
    pt.add_argument("--n", type=int, default=10)

    sub.add_parser("breaches", help="Show only the receipts where the tier soft-cap was tripped")

    ps = sub.add_parser("since", help="Filter receipts to entries since an ISO date")
    ps.add_argument("date", help="ISO date prefix, e.g. 2026-05-01")

    args = p.parse_args(argv[1:])
    if args.cmd == "budgets":
        print(f"{'Tier':<6} {'Budget USD':>12}  {'Breach @':>12}")
        for t, b in TIER_BUDGETS_USD.items():
            print(f"{t:<6} ${b:>11,.4f}  ${b * BUDGET_BREACH_MULTIPLIER:>11,.4f}")
        return 0
    if args.cmd == "rollup":
        print(json.dumps(rollup_efficiency(), indent=2))
        return 0
    if args.cmd == "recent":
        for r in load_receipts(limit=args.n):
            print(json.dumps(r, ensure_ascii=False))
        return 0
    if args.cmd == "audit":
        report = audit_transcript(args.transcript)
        print(json.dumps(report, indent=2))
        return 0 if "error" not in report else 2
    if args.cmd == "top":
        print(json.dumps(top_spenders(by=args.by, n=args.n), indent=2))
        return 0
    if args.cmd == "breaches":
        for r in breach_rows():
            print(json.dumps(r, ensure_ascii=False))
        return 0
    if args.cmd == "since":
        for r in receipts_since(args.date):
            print(json.dumps(r, ensure_ascii=False))
        return 0
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(_main(sys.argv))
