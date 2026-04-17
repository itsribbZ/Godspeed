# Godspeed

**A Claude Code workflow trigger backed by Toke — a routing classifier and multi-agent orchestration engine.**

Type `godspeed` in a Claude Code session, the Toke engine activates for the rest of the turn: each prompt is scored on complexity (S0–S5), routed to the cheapest model that will handle it well, and — for complex tasks — decomposed into parallel Sonnet workers whose synthesis is critic-gated before it lands in a self-improving memory.

Zero fork of Claude Code. Everything wires in through the hook API.

---

## What you get

| | |
|---|---|
| **Cost** | ~30–50% measured savings at quality parity. $750/month saved on $15K/month Opus spend via subagent routing alone. |
| **Accuracy** | Classifier scores 69.0% exact on a 200-prompt held-out eval. Beats the best naive baseline by +31.5 percentage points. |
| **Latency** | Fast-path hook at ~90 ms warm, ~160 ms cold. |
| **Compounding** | Every successful synthesis lands in a vector-embedded memory. Next session's similar prompt retrieves the prior answer in milliseconds. |

Reproduce the benchmark locally: `python toke/automations/brain/eval/brain_vs_baselines.py --json out.json`.

---

## Install (one command)

```bash
git clone https://github.com/<your-username>/godspeed
cd godspeed

# macOS / Linux / Git Bash on Windows
bash install.sh

# Windows PowerShell
.\install.ps1
```

The installer:
1. Copies Toke's 16 skills + 2 slash commands into `~/.claude/`
2. Syncs the routing manifest (TOML → JSON)
3. Runs the 65-test verification suite
4. Prints the `settings.json` hook block you need to paste

After install, set `TOKE_ROOT` in your shell profile (the installer prints the correct value), add the hook block to `~/.claude/settings.json`, and start a new Claude Code session. Try:

```
/brain-score "refactor my distributed cache across 4 files"
# → Tier: S4 | Model: opus | Effort: high

godspeed
# → activates the full Toke pipeline for this turn
```

---

## Repo layout

```
godspeed/
├── README.md          ← this file (the trigger pitch)
├── install.sh         ← one-command install (macOS / Linux / Git Bash)
├── install.ps1        ← Windows PowerShell installer
├── LICENSE            ← MIT
└── toke/              ← the engine
    ├── README.md      ← detailed architecture + design docs
    ├── skills/        ← 16 Claude Code skills (installer copies to ~/.claude/skills/)
    ├── commands/      ← 2 slash commands (installer copies to ~/.claude/commands/)
    ├── hooks/         ← Claude Code lifecycle hook scripts
    ├── automations/   ← classifier + orchestrator + maintenance agents
    ├── pipeline/      ← 8-stage measurement of Claude Code internals
    ├── tokens/        ← cost-accounting tools
    └── research/      ← literature review that fed the classifier design
```

Godspeed (the trigger) is one skill inside `toke/skills/`. It's what fires when you type the word. Everything else in `toke/` is the machinery that skill commands.

---

## Deeper docs

For architecture, design decisions, reproducible benchmarks, references, and usage examples, see **[toke/README.md](toke/README.md)**.

## License

MIT. See `LICENSE`.
