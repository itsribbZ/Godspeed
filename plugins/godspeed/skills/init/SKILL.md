---
name: init
description: >
  Session initialization. Scans the current folder, detects the project type,
  reads CLAUDE.md / README / project_status / MEMORY, loads shared protocols +
  learnings grep-first, runs an ecosystem health check, tails the previous
  session's status, and prints a one-screen briefing with a project
  description, extracted project rules, and session-start context. Companion
  to close-session — init loads, close-session saves.
model: sonnet
---

# Init — Session Briefing + Health

Point init at a folder, get back a project description and the context you
need to start working. Pairs with `close-session` so the two together form a
lossless session loop.

## Trigger

"init", "/init", "start session", "initialize", "begin session", "init this project"

## Phase 0: Load Foundation (grep-first — keep context light)

Never bulk-read the shared files. Pull only the entries tagged for init or ALL:

```bash
grep -B1 -A10 "applies_to.*init\|applies_to.*ALL" \
  ${CLAUDE_PLUGIN_ROOT}/shared/_shared_protocols.md 2>/dev/null

grep -B1 -A10 "applies_to.*init\|applies_to.*ALL" \
  ${CLAUDE_PLUGIN_ROOT}/shared/_shared_learnings.md 2>/dev/null
```

Skip silently if the shared files don't exist — init must never block on missing
context.

## Phase 1: Scan the Folder

Figure out what project this is. One parallel batch — don't iterate:

```bash
echo "CWD: $PWD"
ls -A | head -30
```

Then detect the project type from signal files (first match wins, multiple signals
reported as "multi-stack"):

| Signal file(s) | Project type |
|----------------|--------------|
| `package.json` | Node / TypeScript |
| `pyproject.toml`, `requirements.txt`, `setup.py` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `*.uproject`, `Source/*/*.Build.cs` | Unreal Engine 5 |
| `CMakeLists.txt` | C / C++ |
| `*.csproj`, `*.sln` | C# / .NET |
| `Gemfile` | Ruby |
| `pom.xml`, `build.gradle` | Java / Kotlin |
| `.claude-plugin/plugin.json` | Claude Code plugin |

If it's a git repo, grab the state (one call, bounded output):

```bash
git -C "$PWD" log --oneline -5 2>/dev/null
git -C "$PWD" status --short 2>/dev/null | head -20
git -C "$PWD" branch --show-current 2>/dev/null
```

Skip git calls cleanly if not a repo.

## Phase 2: Load Prior Context

Read files that carry session-to-session context, all in one parallel batch.
Read only the tail of long files — the latest entries are what matters at
session start.

| File | Read pattern | Purpose |
|------|--------------|---------|
| `./CLAUDE.md` | full read if < 5K, else tail 200 lines | **Project rules + personal instructions — binding for the session** |
| `./README.md` | tail 100 lines | Project overview / description |
| `./project_status.md` | tail 150 lines | Most recent session entry |
| `./MEMORY.md` | full read (index file, should stay small) | Memory index |
| `./.claude/settings.json` | full read if present | Hooks, permissions, env vars |

If a file is missing, note it and continue — don't fail.

### Learn from CLAUDE.md (if present)

`CLAUDE.md` is project-level instructions the author wrote for Claude Code.
Treat it as binding for everything that follows in this session. Claude Code
auto-loads it into context — init's job is to **extract the important bits
into the briefing** so the user can confirm they're loaded and the
subsequent work obeys them.

Pull these signals from CLAUDE.md:

- **Sacred rules** / "must never" / "always" directives
- **Preferred tools or commands** (e.g. "use ripgrep not grep", "use pnpm")
- **Style rules** (e.g. commit message format, comment policy, file-layout rules)
- **Forbidden actions** (e.g. "don't run migrations", "don't push to main")
- **Project-specific terminology / concepts**
- **Any explicit "when X, do Y" protocols**

These surface in the Phase 4 briefing under `PROJECT RULES` so the user
verifies the skill absorbed them and subsequent work follows them.

Extract the "Where You Left Off" signal from `project_status.md`: the header
and body of the most recent `## Session:` block.

## Phase 3: Ecosystem Health Check

Fast (<5s), non-blocking, reports inline.

### Learning pipeline counts

Check the shipped compound-learning skills. Any skill with <5 entries AFTER 10+
invocations is probably skipping its learning-write — flag for investigation:

```bash
for skill in devTeam profTeam holy-trinity godspeed blueprint brain cycle close-session; do
  count=$(grep -c '^###' ${CLAUDE_PLUGIN_ROOT}/skills/$skill/_learnings.md 2>/dev/null || echo 0)
  printf '  %-14s %s entries\n' "$skill" "$count"
done
```

Users should extend this list as they add skills that do compound learning.

### Staleness scan (optional — skip if `_shared_learnings.md` is small)

```bash
THRESHOLD_60=$(date -d '60 days ago' +%Y-%m-%d 2>/dev/null || date -v-60d +%Y-%m-%d 2>/dev/null)
STALE_60=$(grep -oP '"staleness_check": "\K[^"]+' \
  ${CLAUDE_PLUGIN_ROOT}/shared/_shared_learnings.md 2>/dev/null | \
  awk -v t="$THRESHOLD_60" '$1 < t' | wc -l)
echo "Staleness: ${STALE_60:-0} entries older than 60d"
```

### Brain telemetry snapshot

```bash
DECISIONS=$(wc -l < ~/.claude/telemetry/brain/decisions.jsonl 2>/dev/null || echo 0)
TICK=$(cat ~/.claude/telemetry/brain/godspeed_count.txt 2>/dev/null || echo 0)
echo "Brain: ${DECISIONS} decisions logged, godspeed tick ${TICK}"
```

Any `wc`/`cat` failures default to 0 — Brain telemetry is optional context, never load-bearing for init.

## Phase 4: Briefing Report

One-screen summary. This is the user-facing output — everything above this
is internal gathering. Render as a single monospaced block:

```
═══════════════════════════════════════════════════════════════
  INIT — [PROJECT NAME OR CWD] — [DATE]
═══════════════════════════════════════════════════════════════

  PROJECT DESCRIPTION
  ───────────────────
   Type:        [Node / Python / UE5 / multi-stack / unknown]
   Root:        [$PWD]
   Summary:     [1-2 sentences from README.md or CLAUDE.md]
   Stack:       [key deps pulled from package.json/pyproject/etc.]

  GIT STATE (if repo)
  ────────────────────
   Branch:      [current branch]
   Recent:      [last 3 commit subjects]
   Uncommitted: [N files changed] — [list of top 5 paths]

  PROJECT RULES (from CLAUDE.md, if present)
  ──────────────────────────────────────────
   [Extracted binding rules — sacred rules, style guides, forbidden
    actions, preferred tools, protocols. If no CLAUDE.md: "no
    project-level rules file — defaults apply".]

  WHERE YOU LEFT OFF
  ──────────────────
   [Most recent session entry from project_status.md, or "no prior
    session log — this is a fresh project"]

  ECOSYSTEM HEALTH
  ────────────────
   Learning pipelines: [per-skill counts]
   Staleness:          [N entries >60d / all fresh]
   Brain:              [N decisions, tick N]

  SESSION CONTEXT
  ───────────────
   Shared protocols:   [applies_to=init entries loaded, count]
   Shared learnings:   [applies_to=init entries loaded, count]
   CLAUDE.md:          [loaded / not present]
   MEMORY.md:          [index with N entries loaded / not present]

  SUGGESTED NEXT STEP
  ───────────────────
   [Derive from project_status.md's "Next Session" block if present;
    otherwise pick from uncommitted git changes; otherwise ask the user
    what to work on.]

═══════════════════════════════════════════════════════════════
```

After rendering, stop. Don't dispatch to any downstream tool — wait for the
user to say what they want. Init is a briefing, not an orchestrator.

## Rules

1. **Never block on a missing file.** Every Read/grep/git call must degrade cleanly.
2. **Never bulk-read `_shared_learnings.md` or `_shared_protocols.md`.** Grep-first — they can be tens of KB.
3. **Never dispatch to another skill.** Init reports; it doesn't execute. The user drives the next step.
4. **Never write files.** Init is read-only. Close-session is the writer.
5. **Token budget:** keep total init turn under ~5K tokens loaded. Grep outputs are bounded; file tails are bounded.
6. **Session context belongs to the user's prompt that follows init.** The briefing is the handoff — don't try to "continue" prior work automatically.

## Init ↔ Close-Session Loop

| Init Reads | Close-Session Writes |
|------------|----------------------|
| project_status.md (most recent session) | project_status.md (new session entry on close) |
| MEMORY.md index | MEMORY.md (new entries on close) |
| CLAUDE.md | CLAUDE.md (new rules if durable insights surfaced) |
| `_learnings.md` (grep, skill-specific) | `_learnings.md` (new entries per invoked skill) |
| `_shared_learnings.md` (grep, applies_to=init) | `_shared_learnings.md` (cross-skill promotions) |
| Brain telemetry (decisions count + tick) | Brain telemetry snapshot in session status |
| Git state (branch + recent commits) | Git snapshot in session status |

The two together give a session a clean start and a clean end with the minimum
token cost at both boundaries.
