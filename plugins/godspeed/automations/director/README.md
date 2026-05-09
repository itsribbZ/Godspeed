# Director — Domain-Axis Agent Routing

The Director maps incoming tasks to a **division** (research / debug / etc.) and the right **agent persona** within that division. It complements Brain (which handles severity tier S0-S5) — Brain says *how hard*, Director says *which domain*.

## What ships in this directory

| File | Purpose |
|---|---|
| `agents/_SCHEMA.md` | Agent definition schema (v1.0) |
| `agents/calliope_synthesizer.json` | Web + local research synthesis with T1-T3 citations |
| `agents/clio_archaeologist.json` | Codebase archaeology — call sites, dependency graphs, dead-code detection |
| `agents/urania_analyst.json` | Numeric telemetry analysis with reproducible commands |
| `agents_manifest.json` | Top-level registry — every agent file must be listed here |

## How it wires up

1. **Define an agent** as a JSON file in `agents/<name>.json` matching `_SCHEMA.md`.
2. **Register it** in `agents_manifest.json` with name + division + parent skill + status.
3. **Invoke it** via `agent_runner.py invoke <name> --task "..." --mode <dry-run|live|claude-code>`.

The three modes:
- `dry-run` (default — **zero API cost**): builds the full prompt envelope, returns mock response, validates structure
- `live`: calls Anthropic API directly (requires `ANTHROPIC_API_KEY`), enforces Cost Guard mid-flight USD ceiling
- `claude-code`: emits a structured dispatch payload for the calling Claude Code session to relay via the Agent tool (zero direct API cost)

## The three starter agents

These are **research-division** personas — read-only by mandate, no write operations. Drop in additional agents for other divisions (debug, marketing, etc.) using the same pattern.

| Agent | Sweet spot | Sample triggers |
|---|---|---|
| **calliope_synthesizer** | "What does the research say about X" — broad parallel-safe synthesis | "research", "deep dive", "synthesize", "what's the state of" |
| **clio_archaeologist** | "Find all call sites of Y" — file:line maps with grep-verified evidence | "map how", "find all callers", "trace the data flow", "dead code" |
| **urania_analyst** | "How many / what percentage / cost breakdown" — numeric telemetry | "how many", "what percentage", "fire rate", "cost breakdown" |

All three target ~3K-token output, run on Sonnet, and ship cost-guarded under tier S2 ($0.10 ceiling per invocation).

## Adding your own agent

1. Copy one of the three starters as a template
2. Edit `name`, `role`, `system_prompt`, `trigger_signals`, `success_metrics`
3. Add an entry to `agents_manifest.json`
4. Test dry-run: `python ../homer/agent_runner.py invoke <name> --task "test" --mode dry-run`
5. When ready, switch to `--mode live` (or rely on Claude Code session dispatch via `--mode claude-code`)

## Sacred-rule alignment

- **Rule 2** (non-destructive): research agents are read-only by mandate — never edit files
- **Rule 6** (no creative): persona prompts are *definitions*, not generative content
- **Rule 11** (AAA): every agent has system_prompt ≥ 800 chars + ≥ 5 trigger signals + measurable success_metrics

## Telemetry

Every invocation writes one JSONL row to `~/.claude/telemetry/brain/agent_invocations.jsonl`. Cost-guarded receipts land in `cost_efficiency.jsonl` (see `automations/homer/cost_guard.py`).
