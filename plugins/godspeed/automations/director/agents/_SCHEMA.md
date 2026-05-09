# Agent Schema (v1.0)

Real subagent persona definitions. Each `<name>.json` defines one agent — its system prompt, tool grants, skill wrappers, trigger signals, success metrics, and per-agent learnings file.

## Required fields

| Field | Type | Description |
|---|---|---|
| `name` | string | Unique agent identifier (snake_case). Becomes the JSON filename. |
| `division` | string | Owning division (`research`, `debug`, etc.). |
| `role` | string | One-line role summary (≤120 chars). |
| `model` | string | `haiku` / `sonnet` / `opus` — invocation model. |
| `system_prompt` | string | Full persona prompt. Includes: charter, sacred-rule overrides, reasoning style, output format. |
| `tool_grants` | string[] | Allowed Claude Code tools (`Read`, `Edit`, `Bash`, `Grep`, etc.). Informational; enforced at dispatch. |
| `skill_wrappers` | string[] | Existing skills this agent reaches into for context. Loaded as context, not invoked. |
| `trigger_signals` | object[] | Phrase + weight signals for sub-dispatch within division. `[{"phrase": "research", "weight": 0.85}, ...]` |
| `success_metrics` | object | Per-agent KPIs (target values measurable from telemetry). |
| `_learnings_path` | string | Relative path to per-agent _learnings.md. |
| `version` | string | Schema version (currently `1.0`). |

## Optional fields

| Field | Type | Description |
|---|---|---|
| `max_thinking_budget` | int | Sonnet/Opus extended thinking budget in tokens. Default per-tier. |
| `tool_result_truncation_chars` | int | Truncate tool output to N chars before next iteration (saves cache cost). |
| `anti_signals` | object[] | Negative phrase weights (suppresses dispatch when matched). |
| `sacred_rule_overrides` | string[] | Agent-specific sacred-rule reinforcements. |
| `output_contract` | object | Structured output expectations (verdict, citations, etc.). |
| `parent_skill` | string | If agent is a focused persona of an existing skill, name it. |
| `created` | string | ISO date created. |
| `scan_date` | string | Last review date. |

## Example minimal agent

```json
{
  "name": "doc_summarizer",
  "division": "research",
  "role": "Summarize a markdown doc into bullet receipts with file:line citations",
  "model": "sonnet",
  "version": "1.0",
  "system_prompt": "You are a Documentation Summarizer...",
  "tool_grants": ["Read", "Grep"],
  "skill_wrappers": ["scanner"],
  "trigger_signals": [
    {"phrase": "summarize doc", "weight": 0.95},
    {"phrase": "tldr this file", "weight": 0.90}
  ],
  "success_metrics": {
    "citation_compliance": {"target": 1.0, "source": "agent_invocations.jsonl"}
  },
  "_learnings_path": "_learnings/doc_summarizer.md",
  "parent_skill": "scanner"
}
```

## Invocation contract

Agents are invoked via `automations/homer/agent_runner.py invoke <name> --task "..."`.

Three modes:
1. **`--mode dry-run`** (default — zero API cost): builds the full prompt envelope, returns mock response, validates structure
2. **`--mode live`**: calls Anthropic API with persona prompt + task. Requires `ANTHROPIC_API_KEY`. Cost-guarded under tier ceiling.
3. **`--mode claude-code`**: emits a structured dispatch payload for the calling Claude Code session to relay via the Agent tool. Zero direct API cost.

## Telemetry

Every invocation writes one JSONL line to `~/.claude/telemetry/brain/agent_invocations.jsonl`:

```json
{"ts": "2026-05-08T...", "agent": "doc_summarizer", "division": "research",
 "mode": "dry-run|live|claude-code", "task_hash": "...", "session_id": "...",
 "model": "sonnet", "input_tokens": 0, "output_tokens": 0, "duration_ms": 0,
 "success": true|false, "verdict": "PASS|SOFT_FAIL|HARD_FAIL|UNKNOWN"}
```

Cost-guarded receipts (LIVE mode) write to `~/.claude/telemetry/brain/cost_efficiency.jsonl`.

## Sacred Rule alignment

- **Rule 4** (only-asked): agents read their own JSON + telemetry; never modify division specs or other agents
- **Rule 5** (diagnostics are features): agent_invocations.jsonl is observability; never delete
- **Rule 6** (no creative): system_prompts are persona definitions, NOT generative content
- **Rule 11** (AAA): every shipped agent has system_prompt ≥ 800 chars + ≥ 5 trigger signals + measurable success_metrics
