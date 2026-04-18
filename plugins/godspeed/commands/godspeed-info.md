---
description: Render the godspeed pipeline overview — flow, tools, brain routing, triggers, and active sacred rules. Read-only, no execution.
---

Invoke the `godspeed:godspeed` skill in **info mode** to render the complete pipeline summary.

Instructions for the model:
1. Read `~/.claude/telemetry/brain/godspeed_count.txt` for the current tick count (fallback `0` if missing).
2. Compute `next_scan_at` = smallest multiple of 33 strictly greater than current tick.
3. Compute `runs_away` = `next_scan_at` − current tick.
4. Render the pipeline ASCII diagram from `godspeed:godspeed` SKILL.md's "Info Mode — Pipeline Summary" section with live tick values substituted.
5. Stop after rendering. Do NOT fire Phase -1 tick. Do NOT triage. Info mode is read-only metadata.

The render should show: execution flow phases, tier-ranked tool roster, brain routing layers, activation triggers, and the currently-active sacred rules.
