---
description: Display the current godspeed/Brain routing manifest — weights, thresholds, tier→model mapping, keyword lists, guardrails, and skill tier assignments. All values are tunable by editing the TOML directly.
---

Display the current Brain routing manifest settings so the user can see what's tunable.

Instructions for the model:
1. Read `${CLAUDE_PLUGIN_ROOT}/automations/brain/routing_manifest.toml` with the `Read` tool.
2. Render a compact summary organized by section:
   - **Signal weights** (`[weights]`) — 10 signals with their percentage contributions to the final score
   - **Tier thresholds** (`[thresholds]`) — score boundaries for S0/S1/S2/S3/S4
   - **Tier → model mapping** (`[tier_map.Sn]`) — model + effort + extended-thinking budget per tier
   - **Keyword lists** (`[keywords]`) — reasoning/multi-step/code-action/ambiguity/tool-calls triggers (counts per list)
   - **Guardrails** (`[guardrails.*]`) — active hard-minimum-score overrides (list names + descriptions)
   - **Skill tier overrides** (`[skills]`) — explicit S-tier assignments for shipped skills
3. At the bottom, print: `To tune: edit ${CLAUDE_PLUGIN_ROOT}/automations/brain/routing_manifest.toml, then run: python ${CLAUDE_PLUGIN_ROOT}/automations/brain/manifest_to_json.py`
4. Keep the output scannable — tables or compact lists, no walls of prose.

This command is read-only — do NOT modify the manifest. Display values exactly as stored.
