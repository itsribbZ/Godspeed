---
description: Render the godspeed pipeline overview — flow, tools, brain routing, cost guard, triggers, and active sacred rules. Read-only, no execution.
allowed-tools: Read
---

# /godspeed-info — Pipeline Overview

Render the godspeed pipeline summary. **Read-only** — does not trigger execution mode.

## Execution

1. Read `~/.claude/telemetry/brain/godspeed_count.txt` with the `Read` tool to get the current tick count. Fallback to `0` if missing or unreadable.
2. Compute `next_scan_at` = smallest multiple of 33 strictly greater than current tick. (current=0 → 33; current=5 → 33; current=33 → 66; current=40 → 66.)
3. Compute `runs_away` = `next_scan_at - current_tick`.
4. Print the template below verbatim inside a single fenced code block, substituting `{TICK}` / `{NEXT_SCAN}` / `{RUNS_AWAY}` with the live values.
5. After rendering, write one short closing line (e.g. `Info mode rendered. Say "godspeed" for execution mode.`) and **STOP**. No further tool calls. No triage. No Phase -1 tick. Info mode is render-and-stop.

## Template (substitute live values for `{TICK}` / `{NEXT_SCAN}` / `{RUNS_AWAY}`)

```
═══════════════════════════════════════════════════════════════
  GODSPEED v4.10 — MAX EXECUTION MODE
═══════════════════════════════════════════════════════════════

  PIPELINE FLOW
  ─────────────

   [-1]   TICK              Self-audit counter (every 33 ticks → brain scan)
                            current: {TICK}  next: {NEXT_SCAN}  ({RUNS_AWAY} away)
          │
          ▼
   [0.5]  BRAIN             Severity classify S0–S5 → tier→model bind
          │                 (S0/S1=Haiku · S2/S3=Sonnet · S4/S5=Opus)
          │                 S3+ → auto-dispatch Zeus
          │
          ▼
   [1-3]  TRIAGE → ROUTE → DEPLOY
          │                 Domain-adaptive priority P0→P3, Pipeline Router,
          │                 parallel tool execution where possible
          │
          ▼
   [3i]   COST GUARD        Mid-flight budget enforcement (1.5× soft-cap)
          │                 Verdict: OK / BUDGET_EXCEEDED
          │                 Receipts → ~/.claude/telemetry/brain/cost_efficiency.jsonl
          │
          ▼
   [4]    ESCALATE          L1 narrow → L2 instrument → L3 research →
          │                 L3.5 advisor (Sonnet stuck → Opus rescue) →
          │                 L4 ask user → L5 flag blocker
          │
          ▼
   [5]    RECONCILE         Zero-missed-tasks verification
          │
          ▼
   [6]    LEARN             zeus gate-write → Oracle score → Mnemos Recall

  SHIPPED SKILLS (18 total — domain-agnostic methodology)
  ───────────────────────────────────────────────────────

   HOMER PANTHEON (orchestrator-worker stack)
       zeus            L2 Orchestrator — decomposes S3+ tasks
       calliope        L3 Epic Research Muse (web + synthesis)
       clio            L3 Code Archaeology Muse (file:line maps)
       urania          L3 Measurement Muse (telemetry receipts)
       sybil           L4 Advisor escalation (advisor_20260301)
       mnemos          L5 3-tier memory (Core / Recall / Archival)
       oracle          L7 Critic — scores synthesis, gates writes
       brain           L1 Severity classifier (S0-S5 router)

   PIPELINE SKILLS (methodology)
       holy-trinity    Diagnose → Research → Implement → Verify
       devTeam         Code architecture scoring (7 Laws)
       profTeam        Multi-agent parallel research engine
       professor       Single-topic deep research + PDF
       blueprint       Implementation plan from codebase
       cycle           3-pass blueprint refinement

   UTILITY SKILLS
       close-session   Session closure + learning persistence
       verify          Build / test verification (multi-stack)
       init            Project initialization router
       godspeed        This skill — max-execution mode

  COST GUARD BUDGETS (Phase 3i, per agent invocation)
  ───────────────────────────────────────────────────

       S0 $0.005    S1 $0.02    S2 $0.10
       S3 $0.50     S4 $2.00    S5 $5.00
       1.5× soft-cap → BUDGET_EXCEEDED verdict mid-flight

  BRAIN ROUTING (always active, zero config)
  ──────────────────────────────────────────

       Severity tiers   S0-S2 → direct tool   |   S3-S5 → Zeus orchestrator
       Subagents        Sonnet via CLAUDE_CODE_SUBAGENT_MODEL env var
       Skills           Pinned per skill frontmatter (S-tier)
       Advisor API      L3.5 — Sonnet stuck → Opus rescue (max 2/session)
       Self-audit       every 33 ticks → inline `brain scan`

  SLASH COMMANDS
  ──────────────

       /godspeed-info        This pipeline summary (you are here)
       /godspeed-settings    Render current routing manifest (weights, tiers, guardrails)
       /brain-score <text>   Classify any prompt on the S0-S5 scale

  TRIGGERS
  ────────

       "godspeed" / GODSPEED   Full max execution mode
       "stuck" mid-task        L3.5 advisor escalation
       Every 33 ticks          Inline `brain scan` self-audit

  SACRED RULES ACTIVE (11)
  ────────────────────────

       #1  Truthful           #2  No delete           #3  No revert
       #4  Only-asked         #5  Diag = feature      #6  No creative
       #7  Edit only          #8  No auto-close       #9  No menus
       #10 godspeed = command #11 AAA quality

═══════════════════════════════════════════════════════════════
```

After rendering, output one closing line and stop. Do NOT continue into Core Rules, do NOT triage, do NOT execute anything. Info mode is render-and-stop.
