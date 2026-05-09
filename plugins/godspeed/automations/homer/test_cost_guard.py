#!/usr/bin/env python3
"""
test_cost_guard.py — Phase 3i cost / efficiency guard regression harness.

Covers:
- pure cost_guard math (budgets, breach, tier inference, cache rate)
- receipt build + write round-trip
- invoke_live mid-flight BUDGET_EXCEEDED via stubbed Anthropic client

The mid-flight test stubs `anthropic` in sys.modules BEFORE agent_runner is
imported so invoke_live picks up the fake. The stub returns a high-token
response on first iteration, which trips an S0 ($0.005) budget.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import types
from pathlib import Path

THIS = Path(__file__).resolve()
HOMER_DIR = THIS.parent
sys.path.insert(0, str(HOMER_DIR))

import cost_guard  # noqa: E402


# ----------------------------------------------------------------------------
# 1. Pure-function checks (mirror cost_guard.is_breach + budget_for_tier matrix)
# ----------------------------------------------------------------------------
def test_pure_functions() -> None:
    assert cost_guard.is_breach(0.15, 0.1) is True
    assert cost_guard.is_breach(0.10, 0.1) is False
    assert cost_guard.is_breach(0.149, 0.1) is False
    assert cost_guard.is_breach(0.0, 0.1) is False
    assert cost_guard.is_breach(1.0, 0.0) is False

    assert cost_guard.budget_for_tier("S0") == 0.005
    assert cost_guard.budget_for_tier("S5") == 5.0
    assert cost_guard.budget_for_tier(None) == 0.1
    assert cost_guard.budget_for_tier("S99") == 0.1
    assert cost_guard.budget_for_tier("s2") == 0.1

    assert cost_guard.tier_for_model("haiku")  == "S1"
    assert cost_guard.tier_for_model("sonnet") == "S2"
    assert cost_guard.tier_for_model("opus")   == "S4"
    assert cost_guard.tier_for_model(None)     == "S2"

    assert cost_guard.cache_hit_rate(0, 0, 0) is None
    assert cost_guard.cache_hit_rate(100, 900, 0) == 0.9
    assert cost_guard.cache_hit_rate(1000, 0, 0) == 0.0


# ----------------------------------------------------------------------------
# 2. Receipt round-trip (build → write → load → rollup)
# ----------------------------------------------------------------------------
def test_receipt_roundtrip() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        original_path = cost_guard.RECEIPT_PATH
        cost_guard.RECEIPT_PATH = Path(tmp) / "cost_efficiency.jsonl"
        try:
            ok = cost_guard.write_receipt(cost_guard.build_receipt(
                agent="alpha", tier="S2", actual_cost_usd=0.05,
                iterations=3, verdict="OK", session_id="sess1",
            ))
            assert ok, "write_receipt returned False"
            ok2 = cost_guard.write_receipt(cost_guard.build_receipt(
                agent="beta", tier="S2", actual_cost_usd=0.16,
                iterations=2, verdict="BUDGET_EXCEEDED", session_id="sess1",
            ))
            assert ok2

            rows = cost_guard.load_receipts()
            assert len(rows) == 2
            assert rows[0]["agent"] == "alpha"
            assert rows[1]["breach"] is True

            roll = cost_guard.rollup_efficiency(rows)
            assert roll["receipt_count"] == 2
            assert abs(roll["total_actual_usd"] - 0.21) < 1e-6
            assert abs(roll["total_budget_usd"] - 0.20) < 1e-6
            assert roll["breach_count"] == 1
            assert roll["breach_rate"] == 0.5
            assert "alpha" in roll["by_agent"]
            assert "beta" in roll["by_agent"]
            assert roll["by_tier"]["S2"]["fires"] == 2
        finally:
            cost_guard.RECEIPT_PATH = original_path


# ----------------------------------------------------------------------------
# 3. Mid-flight BUDGET_EXCEEDED via stubbed Anthropic client
# ----------------------------------------------------------------------------
class _StubUsage:
    """Mimics anthropic.types.Usage just enough for invoke_live to read."""
    def __init__(self, input_tokens: int, output_tokens: int):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_read_input_tokens = 0
        self.cache_creation_input_tokens = 0


class _StubBlock:
    def __init__(self, text: str):
        self.text = text


class _StubResponse:
    def __init__(self, input_tokens: int, output_tokens: int, text: str = "ok"):
        self.usage = _StubUsage(input_tokens, output_tokens)
        self.stop_reason = "end_turn"  # not tool_use → loop exits naturally
        self.content = [_StubBlock(text)]


class _StubMessages:
    def __init__(self, response: _StubResponse):
        self._response = response

    def create(self, **kwargs):
        return self._response


class _StubClient:
    def __init__(self, response: _StubResponse):
        self.messages = _StubMessages(response)


def _install_anthropic_stub(response: _StubResponse) -> None:
    fake_module = types.ModuleType("anthropic")

    class Anthropic:
        def __init__(self, api_key=None, **_):
            self._api_key = api_key

        # Allow attribute access used inside invoke_live.
        def __getattr__(self, name):
            if name == "messages":
                return _StubMessages(response)
            raise AttributeError(name)

    fake_module.Anthropic = Anthropic
    sys.modules["anthropic"] = fake_module


def test_invoke_live_breach() -> None:
    # Need an API key in env for invoke_live to enter the live path (it
    # short-circuits to dry-run otherwise). The stub never validates the key.
    os.environ.setdefault("ANTHROPIC_API_KEY", "test-stub-key")

    # 200K input × $5/MTok opus = $1.00 (way over S0's $0.005 / breach $0.0075).
    # Sized so any S<3 tier breaches on first iteration.
    response = _StubResponse(input_tokens=200_000, output_tokens=0, text="stub-pass")
    _install_anthropic_stub(response)

    if "agent_runner" in sys.modules:
        del sys.modules["agent_runner"]
    import agent_runner  # type: ignore  # picks up stubbed anthropic

    # Hand-craft a payload that mimics build_invocation_payload output.
    payload = {
        "agent": "stub_agent",
        "division": "debug",
        "model": "opus",
        "system_prompt": "system" * 50,  # ≥ 200 chars
        "user_task": "run breach scenario",
        "tool_grants": [],
        "skill_wrappers": [],
        "max_thinking_budget": 0,
        "tool_result_truncation_chars": 8000,
        "task_hash": "stubhash",
        "tier": "S0",
        "budget_usd": 0.005,
    }
    result = agent_runner.invoke_live(payload, max_iterations=3)
    assert result["mode"] == "live", f"expected live mode, got {result['mode']!r}"
    assert result["verdict"] == "BUDGET_EXCEEDED", (
        f"expected BUDGET_EXCEEDED, got {result['verdict']!r}"
    )
    assert result["breach"] is True
    assert result["budget_usd"] == 0.005
    assert result["tier"] == "S0"
    assert result["success"] is False
    assert result["iterations"] == 1, "should break on first iteration"


# ----------------------------------------------------------------------------
# 4. Pricing math (compute_cost_from_usage)
# ----------------------------------------------------------------------------
def test_compute_cost_from_usage() -> None:
    # Haiku: $1 input / $5 output per MTok. 1M input + 1M output = $6.00
    cost = cost_guard.compute_cost_from_usage(
        model="haiku", input_tokens=1_000_000, output_tokens=1_000_000,
    )
    assert abs(cost - 6.00) < 1e-6, f"haiku 1M+1M expected $6, got ${cost}"

    # Sonnet: $3/$15. 100K input + 50K output = $0.30 + $0.75 = $1.05
    cost = cost_guard.compute_cost_from_usage(
        model="claude-sonnet-4-7", input_tokens=100_000, output_tokens=50_000,
    )
    assert abs(cost - 1.05) < 1e-6, f"sonnet 100K+50K expected $1.05, got ${cost}"

    # Opus: $15/$75. 10K input + 10K output = $0.15 + $0.75 = $0.90
    cost = cost_guard.compute_cost_from_usage(
        model="opus", input_tokens=10_000, output_tokens=10_000,
    )
    assert abs(cost - 0.90) < 1e-6, f"opus 10K+10K expected $0.90, got ${cost}"

    # Cache pricing — sonnet cache_read $0.30/MTok, cache_write $3.75/MTok
    cost = cost_guard.compute_cost_from_usage(
        model="sonnet", cache_read_tokens=1_000_000, cache_creation_tokens=100_000,
    )
    assert abs(cost - (0.30 + 0.375)) < 1e-6, f"sonnet cache 1M read + 100K write expected $0.675, got ${cost}"

    # Unknown model → falls through to sonnet defaults
    cost = cost_guard.compute_cost_from_usage(
        model="unknown-model", input_tokens=1_000_000, output_tokens=0,
    )
    assert abs(cost - 3.00) < 1e-6, f"unknown model should use sonnet, got ${cost}"

    # Empty / None → 0 cost (sonnet fam, but zero tokens)
    assert cost_guard.compute_cost_from_usage(model=None) == 0.0


# ----------------------------------------------------------------------------
# 5. Transcript audit (synthetic JSONL)
# ----------------------------------------------------------------------------
def test_audit_transcript_synthetic() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        transcript = Path(tmp) / "fake_session.jsonl"
        rows = [
            # Sonnet — small, well under S2 ceiling
            {"message": {"model": "claude-sonnet-4-7", "usage": {
                "input_tokens": 1000, "output_tokens": 500,
                "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0,
            }}},
            # Opus — would breach S4 at 1M+1M ($90)
            {"message": {"model": "claude-opus-4-7", "usage": {
                "input_tokens": 1_000_000, "output_tokens": 1_000_000,
            }}},
            # Haiku — tiny
            {"message": {"model": "claude-haiku-4-5", "usage": {
                "input_tokens": 100, "output_tokens": 50,
            }}},
            # No usage block — should be skipped silently
            {"message": {"model": "sonnet"}},
            # No message block — should be skipped silently
            {"type": "user", "content": "hello"},
        ]
        with open(transcript, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")

        report = cost_guard.audit_transcript(transcript)
        assert report["row_count"] == 3, f"expected 3 audited rows, got {report['row_count']}"
        # Total cost: sonnet ~$0.0105 + opus $90 + haiku ~$0.00035 = ~$90.011
        assert 89.0 < report["total_cost_usd"] < 91.0, f"unexpected total: {report['total_cost_usd']}"
        assert report["by_model"]["sonnet"]["calls"] == 1
        assert report["by_model"]["opus"]["calls"] == 1
        assert report["by_model"]["haiku"]["calls"] == 1
        assert report["would_breach_count"] >= 1, "opus row should have breached S4"
        # Top message cost: opus 1M+1M = $90
        assert report["top_message_costs"][0]["model"] == "opus"
        assert report["top_message_costs"][0]["would_breach"] is True


def test_audit_transcript_missing() -> None:
    report = cost_guard.audit_transcript("/nonexistent/path/foo.jsonl")
    assert "error" in report
    assert report["row_count"] == 0


def test_audit_transcript_partial_corruption() -> None:
    """Bad lines should be collected as errors, not crash the audit."""
    with tempfile.TemporaryDirectory() as tmp:
        transcript = Path(tmp) / "corrupt.jsonl"
        with open(transcript, "w", encoding="utf-8") as f:
            f.write('{"message":{"model":"sonnet","usage":{"input_tokens":100,"output_tokens":50}}}\n')
            f.write('this is not json\n')
            f.write('{"message":{"model":"haiku","usage":{"input_tokens":50}}}\n')
        report = cost_guard.audit_transcript(transcript)
        assert report["row_count"] == 2
        assert len(report["errors"]) == 1


# ----------------------------------------------------------------------------
# 6. Top spenders + breach filter + since filter
# ----------------------------------------------------------------------------
def test_top_spenders_by_agent() -> None:
    rows = [
        {"agent": "alpha", "tier": "S2", "actual_cost_usd": 0.50, "budget_usd": 0.10, "breach": True},
        {"agent": "alpha", "tier": "S2", "actual_cost_usd": 0.05, "budget_usd": 0.10, "breach": False},
        {"agent": "beta",  "tier": "S2", "actual_cost_usd": 0.20, "budget_usd": 0.10, "breach": True},
        {"agent": "gamma", "tier": "S3", "actual_cost_usd": 0.30, "budget_usd": 0.50, "breach": False},
    ]
    top = cost_guard.top_spenders(by="agent", n=10, rows=rows)
    assert len(top) == 3
    # alpha leads at $0.55
    assert top[0]["agent"] == "alpha"
    assert top[0]["fires"] == 2
    assert abs(top[0]["actual_usd"] - 0.55) < 1e-6
    assert top[0]["breaches"] == 1


def test_top_spenders_by_tier() -> None:
    rows = [
        {"agent": "x", "tier": "S2", "actual_cost_usd": 0.10, "budget_usd": 0.10, "breach": False},
        {"agent": "y", "tier": "S2", "actual_cost_usd": 0.20, "budget_usd": 0.10, "breach": True},
        {"agent": "z", "tier": "S3", "actual_cost_usd": 0.05, "budget_usd": 0.50, "breach": False},
    ]
    top = cost_guard.top_spenders(by="tier", n=2, rows=rows)
    assert len(top) == 2
    assert top[0]["tier"] == "S2"
    assert top[0]["fires"] == 2


def test_top_spenders_invalid_by() -> None:
    try:
        cost_guard.top_spenders(by="nonsense", rows=[])
    except ValueError:
        return  # expected
    raise AssertionError("expected ValueError on invalid 'by'")


def test_breach_rows() -> None:
    rows = [
        {"agent": "a", "breach": False},
        {"agent": "b", "breach": True},
        {"agent": "c", "breach": True},
    ]
    out = cost_guard.breach_rows(rows=rows)
    assert len(out) == 2
    assert all(r["breach"] for r in out)


def test_receipts_since() -> None:
    rows = [
        {"agent": "a", "ts": "2026-04-01T00:00:00Z"},
        {"agent": "b", "ts": "2026-05-08T00:00:00Z"},
        {"agent": "c", "ts": "2026-05-09T00:00:00Z"},
    ]
    out = cost_guard.receipts_since("2026-05-01", rows=rows)
    assert len(out) == 2
    assert {r["agent"] for r in out} == {"b", "c"}


# ----------------------------------------------------------------------------
# 7. rollup_efficiency on empty input
# ----------------------------------------------------------------------------
def test_rollup_empty() -> None:
    roll = cost_guard.rollup_efficiency(rows=[])
    assert roll["receipt_count"] == 0
    assert roll["total_actual_usd"] == 0.0
    assert roll["breach_count"] == 0
    assert roll["by_agent"] == {}


# ----------------------------------------------------------------------------
# Entry
# ----------------------------------------------------------------------------
def main() -> int:
    cases = [
        ("pure_functions",            test_pure_functions),
        ("receipt_roundtrip",         test_receipt_roundtrip),
        ("invoke_live_breach",        test_invoke_live_breach),
        ("compute_cost_from_usage",   test_compute_cost_from_usage),
        ("audit_transcript_synth",    test_audit_transcript_synthetic),
        ("audit_transcript_missing",  test_audit_transcript_missing),
        ("audit_transcript_corrupt",  test_audit_transcript_partial_corruption),
        ("top_spenders_by_agent",     test_top_spenders_by_agent),
        ("top_spenders_by_tier",      test_top_spenders_by_tier),
        ("top_spenders_invalid_by",   test_top_spenders_invalid_by),
        ("breach_rows",               test_breach_rows),
        ("receipts_since",            test_receipts_since),
        ("rollup_empty",              test_rollup_empty),
    ]
    failed: list[str] = []
    for name, fn in cases:
        try:
            fn()
            print(f"[PASS] {name}")
        except AssertionError as e:
            print(f"[FAIL] {name}: {e}")
            failed.append(name)
        except Exception as e:
            print(f"[FAIL] {name}: {type(e).__name__}: {e}")
            failed.append(name)
    print("=" * 50)
    if failed:
        print(f"{len(failed)} FAIL: {failed}")
        return 1
    print(f"ALL {len(cases)} PASS — Phase 3i cost guard verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
