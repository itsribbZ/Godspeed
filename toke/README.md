# Toke

**A routing classifier and multi-agent orchestrator for Claude Code.** Sits between your prompts and Anthropic's API. Scores each prompt on a 6-tier complexity scale (S0–S5), routes it to the right model (Haiku / Sonnet / Opus), and decomposes complex tasks into parallel Sonnet workers with critic-gated memory writes. Fully local; the only external call is to the Anthropic API.

---

## Benchmark

The evaluation harness (`automations/brain/eval/brain_vs_baselines.py`) compares the classifier against four naive baselines (majority-class, keyword-only, length-only, random). It does NOT ship a labeled golden set — bring your own as `automations/brain/eval/golden_set.json`:

```json
[
  {"prompt": "list files here", "expected": "S0"},
  {"prompt": "refactor my distributed cache across 4 files", "expected": "S4"}
]
```

Then:

```bash
python automations/brain/eval/brain_vs_baselines.py --json out.json
```

The maintainer's internal eval (299-prompt held-out set, not shipped) scores **75.6% exact / 0.875 weighted, 226/299 exact and 2 wrong** at v2.7. Your numbers will vary by prompt distribution.

**Cost impact (projection, not measurement):** subagent auto-routing on heavy-Opus workloads (~$15K/month spend) projects ~$750/month savings; auto-orchestration on S3+ tasks projects an additional $600–1,200/month at quality parity (per Anthropic's multi-agent research eval — see references). Run `brain scan` against your own telemetry for actuals.

---

## Install

```bash
git clone https://github.com/<your-username>/toke
cd toke

# macOS / Linux / Git Bash on Windows
bash install.sh

# Windows PowerShell
.\install.ps1
```

The installer copies 16 skills and 2 slash commands into `~/.claude/`, syncs the routing manifest (TOML → JSON), and runs the full test suite. Existing skills with the same name are preserved unless `--force` (bash) / `-Force` (PowerShell) is passed — in which case old versions are backed up to `.bak.<timestamp>`.

After install:

1. Add the hook block the installer prints to `~/.claude/settings.json`.
2. Set `TOKE_ROOT` in your shell profile.
3. Start a new Claude Code session and try `/brain-score "refactor my distributed cache across 4 files"` — expect `S4 / opus / high`.

### Requirements

- Python 3.10+ (stdlib only for the core classifier)
- Node.js 18+ (fast-path hook, warm latency ~90 ms)
- Claude Code CLI (the hooks wire into its lifecycle events)
- Optional: `sentence-transformers` for semantic memory search, Ollama for local-LLM fallback

---

## How it works

```
Claude Code prompt
    │
    ▼
UserPromptSubmit hook  ────►  Classifier (stdlib, manifest-driven)
                                 │
                  ┌──────────────┼──────────────┐
                  ▼              ▼              ▼
               S0 – S2        S3 routed      S4 – S5
              (Haiku)      to orchestrator   (Opus)
                                 │
                                 ▼
                          Decompose plan
                                 │
                   ┌─────────────┼─────────────┐
                   ▼             ▼             ▼
                Research   Code-archaeology  Measurement
                  muse         muse            muse         (parallel Sonnet)
                   └─────────────┼─────────────┘
                                 ▼
                         Synthesis + citation check
                                 │
                                 ▼
                         Critic evaluates synthesis
                          (rules + rubric + theater
                           detection)
                                 │
                   ┌─────────────┴─────────────┐
                   ▼                           ▼
           PASS / SOFT_FAIL               HARD_FAIL
                   │                           │
                   ▼                           ▼
          Write to memory store         Block write,
          (SQLite FTS5 + vectors)       return verdict
                   │                    with rule failures
                   ▼
            WAL checkpoint
```

Every classification lands in `~/.claude/telemetry/brain/decisions.jsonl` for cost analysis and drift monitoring.

---

## Stack

| Layer | Technology |
|---|---|
| Classifier | Python standard library, zero external dependencies |
| Fast-path hook | Node.js 18+ (warm ≈ 90 ms, cold ≈ 160 ms) |
| Memory store | SQLite with FTS5 + optional `sentence-transformers` vector embeddings (`all-MiniLM-L6-v2`, 384-d, local) |
| Orchestrator | Python standard library + Claude Code `Agent` tool (Sonnet via `CLAUDE_CODE_SUBAGENT_MODEL` env var) |
| Checkpoint store | SQLite with WAL + retry/backoff |
| Optional local LLM | Ollama + Qwen 2.5 14B (S0–S2 fallback, no API cost) |
| Optional evolution | GEPA-style evolutionary weight tuner for manifest refinement |

---

## Design decisions

1. **Manifest-driven classifier, not learned.** Tier boundaries, signal weights, and guardrails live in a TOML manifest. Every routing decision is auditable in plain text. No opaque model weights to explain to stakeholders.
2. **Fail-open everywhere.** If the classifier crashes, default to Opus. If a hook errors, exit 0 silently. No component of Toke can block a Claude turn.
3. **The critic gates memory writes in code.** A `HARD_FAIL` verdict blocks the memory write inside the Python pipeline function — not by documentation convention. The sacred ordering is enforced by structure.
4. **Sleep-time agents propose, humans decide.** The nightly weight-tuner and theater-auditor never auto-apply changes. Every suggested change is a proposal awaiting explicit approval.
5. **Standard library first.** The core is stdlib only. Optional dependencies are truly optional and fall back gracefully when missing.
6. **Receipts mandatory.** Every accuracy claim in this README is backed by a JSON artifact and a reproducible runner. No benchmark numbers without a way to regenerate them.
7. **Progressive disclosure on memory reads.** Memory search returns snippet-level summaries first; full content is fetched on demand. Measured ~7–10× token reduction on repeated-recall workloads.
8. **Oracle-gated atomic writes.** Memory writes for orchestrator synthesis output run through a single CLI command that collapses "evaluate synthesis" and "write to memory" into one atomic operation, eliminating the fragile pattern of running them as separate steps.

---

## Usage examples

### Classify a prompt

```bash
python automations/brain/brain_cli.py score "design a distributed caching layer"
# Tier: S4 | Model: opus | Effort: high | Score: 0.400
```

### Cost analysis against a 30-day window

```bash
python automations/brain/brain_cli.py scan
# Total spend: $XXXX | Subagent-routing savings projection: $XXX
# (output reflects your own session telemetry — first-time users see $0 until decisions accumulate)
```

### Run the orchestrator synthesis → memory pipeline in Python

```python
from zeus.zeus_pipeline import gate_and_write
from oracle.oracle import Oracle
from mnemos.mnemos import MnemosStore

result = gate_and_write(
    oracle=Oracle(),
    store=MnemosStore(),
    synthesis="...multi-agent synthesis output...",
    topic="caching_analysis",
    citations=["session:run_20260417"],
)
# result.written == True, result.verdict == "PASS", result.entry_id == "recall_..."
```

### Run the same flow from the CLI (atomic)

```bash
python automations/homer/zeus/zeus_cli.py gate-write \
    --topic "caching analysis" \
    --synthesis-file /tmp/synthesis.md \
    --citations "session:run_20260417,decisions.jsonl:200"
```

### Run nightly maintenance agents on demand

```bash
python automations/homer/sleep/sleep_cli.py run all
# Weight tuner + learning distiller + theater auditor — reports land in
# automations/homer/sleep/<agent>/ for review.
```

---

## Project layout

```
toke/
├── README.md                     this file
├── install.sh / install.ps1      one-command installer (bash + PowerShell)
├── .env.example                  env var template
├── skills/                       16 Claude Code skills (installer copies to ~/.claude/skills/)
├── commands/                     2 slash commands (installer copies to ~/.claude/commands/)
├── automations/
│   ├── brain/                    S0-S5 classifier (manifest-driven)
│   ├── homer/                    multi-agent orchestrator (internal codename — see Naming)
│   ├── gepa/                     evolutionary weight tuner
│   ├── local/                    Ollama fallback
│   ├── governance/               audit protocol + threat model
│   └── portability/              migration guide
├── hooks/                        UserPromptSubmit / PostToolUse / SessionEnd
├── pipeline/                     measured Claude Code internals (8 stages documented)
├── tokens/                       token-accounting measurement tools
└── research/                     literature review feeding the classifier design
```

### Naming convention

The multi-agent orchestrator internal codename is **Homer**. Each layer is named after a figure from Greek mythology to serve as a memorable navigation aid — each name reflects the layer's role:

| Codename | Role |
|---|---|
| Zeus | Top-level orchestrator (decomposes, dispatches, synthesizes) |
| Calliope | Research worker (web + synthesis, T1-T3 source citations) |
| Clio | Code-archaeology worker (file:line mapping of existing codebases) |
| Urania | Measurement worker (telemetry, benchmarks, receipts) |
| Sybil | Advisor-escalation wrapper (calls Anthropic's advisor API on hard failures) |
| Mnemos | Three-tier memory store (context-resident / searchable / cold archive) |
| Oracle | Synthesis critic (rule checks, rubric scoring, theater detection) |
| Aurora / Hesper / Nyx | Nightly maintenance agents (weight tuning, learning distillation, theatrical-language auditing) |

The naming is internal-only. External documentation and function signatures use standard industry terms.

---

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `TOKE_ROOT` | cloned repo path | Install location (hooks reference it) |
| `CLAUDE_CODE_SUBAGENT_MODEL` | `sonnet` | Default model for subagents spawned via the Claude Code Agent tool |
| `ANTHROPIC_API_KEY` | — | Required for the advisor escalation path |
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Local-LLM endpoint for the S0–S2 fallback |

See `.env.example` for a complete template.

---

## Testing

```bash
python automations/brain/brain_tests.py            # classifier smoke tests
python automations/homer/mnemos/test_mnemos.py     # memory store (45/45)
python automations/homer/homer_integration_test.py # end-to-end integration (20/20)
```

All three suites pass on a clean install.

---

## References

- Anthropic. "How we built our multi-agent research system." 2025. https://www.anthropic.com/engineering/multi-agent-research-system
- Packer, C. et al. "MemGPT: Towards LLMs as Operating Systems." arXiv:2310.08560. 2023.
- Zhou, Y. et al. "EvolveR: Self-Evolving Agents via Reflection." arXiv:2510.16079. 2025.
- Anthropic Prompt Caching documentation. https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching

---

## License

MIT. See `LICENSE`.

## Contributing

Issues and pull requests welcome. Please run the full test suite (`brain_tests.py`, `test_mnemos.py`, `homer_integration_test.py`) before submitting.
