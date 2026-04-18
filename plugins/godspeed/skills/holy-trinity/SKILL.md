---
name: holy-trinity
description: >
  Supreme diagnose-research-implement-verify engine. Combines devTeam (calibrated diagnosis 
  with regression guard) and profTeam (adaptive agents with ROI tracking) in a convergent loop. 
  Stops when diminishing returns hit OR regression risk exceeds improvement value.
model: opus
effort: high
---

# The Holy Trinity v4.0 — Adaptive Convergent Improvement Engine

## When to Trigger

- User says "holy trinity", "deploy holy trinity", "run holy trinity", "trinity on [topic]"
- User says "upgrade [system]", "self-improve [system]", "make [system] better"
- User wants the complete diagnose → research → implement → verify loop
- When a system, skill, or architecture needs measured improvement, not just research

## Target Type Auto-Presets (v2.0)

Before scoring, auto-detect the target type and load preset scoring dimensions. This eliminates the manual dimension-definition step from v1.0.

### Preset Library (validated across 5+ runs)

| Target Type | Detection Signal | Dimensions (7 × 0-5 = 35 max) |
|-------------|-----------------|-------------------------------|
| **Code/Architecture** | Source files, .h/.cpp, .ts/.tsx | Law1:Simplicity, Law2:DataDriven, Law3:EdgeCases, Law4:Decoupling, Law5:Liability, Law6:Disclosure, Law7:WorkRightFast |
| **Skill/Tool** | SKILL.md, _learnings.md, .claude/skills/ | Reliability, SelfImprovement, CrossSkillIntegration, Resilience, OutputQuality, Efficiency, Extensibility |
| **Game Design** | GDD, design docs, no code target | Coherence, ScopeFeasibility, CoreLoop, Differentiation, Interconnection, TechSpec, PlayerMotivation |
| **Product/Business** | Market analysis, revenue model | MktValidation, CompetitiveGap, RevenueModel, BuildFeasibility, DistributionPath, UniqueAdvantage, ScalePotential |
| **Standalone Tool** | Python/script, standalone app | FeatureCompleteness, Architecture, SafetyReliability, UX, Extensibility, Documentation, Integration |
| **Infrastructure** | CI/CD, deploy, configs | Reliability, Security, Observability, Automation, Recovery, Scalability, Maintainability |
| **Custom** | Cannot auto-detect | Define 7 dimensions in Phase 0 — document rationale |

**Cross-run note**: When running on a target that matches a previous run's type, load that run's scoring calibration notes. If the previous run flagged "dimension X was most impactful", weight it higher.

## The Trinity Loop v2.0

```
Pass N:
  ① devTeam v4.0 DIAGNOSES
     → Calibrated scores + ranked gap list
     → Protected dimensions tagged (score ≥4/5)
     → Regression baseline snapshot

  ② profTeam v4.0 RESEARCHES (targeted)
     → Topic classified from gap descriptions
     → Agent config auto-selected (with ROI data)
     → Smart Cycle compression applied
     → Solutions for top gaps only

  ③ IMPLEMENT (with regression guard)
     → Independent fixes in parallel
     → Dependent fixes sequential
     → Each fix verified against regression baseline
     → Escalation if regression detected

  ④ devTeam v4.0 RE-SCORES
     → Compare to Pass N-1
     → Compute velocity (rate of improvement)
     → Regression check on protected dimensions
     → Net assessment

  ⑤ CONVERGENCE DECISION (velocity-aware)
     → Score delta + velocity trend + regression status
     → CONTINUE / STOP / ESCALATE
```

## Parallel Execution
Follow _shared_protocols.md SS3. Parallelization map for Trinity phases:

| Phase | Parallel batch |
|-------|---------------|
| 0 (Load) | All learnings + project docs + research PDFs |
| 1 (Diagnose) | All Critical + High priority target files |
| 2 (Research) | All profTeam agents |
| 3 (Implement) | All independent fixes |
| 4 (Re-score) | All modified files |

---


**Pre-work**: Follow _shared_protocols.md SS1.

## Quick Trinity Mode (v3.1 — Lightweight Pass)

**Not every target needs the full pipeline.** Quick Trinity is a single-pass mode that skips profTeam research entirely. It's the right tool when the gap is obvious and the fix is known.

### When to Use Quick Trinity
- Target is a single file or module (<500 LOC)
- The gap is clearly diagnosable without research (e.g., missing interface, god class split, naming cleanup)
- User says "quick trinity", "quick pass", "fast trinity", or "just fix it"
- devTeam diagnosis reveals ≤3 gaps AND all are LOW/MEDIUM severity
- The fix doesn't require learning new APIs, patterns, or engine behavior

### When NOT to Use Quick Trinity (Full Trinity Required)
- Target spans multiple modules or systems
- Gaps involve unfamiliar APIs, engine internals, or networking
- Any gap is CRITICAL severity
- User explicitly says "full trinity", "deep trinity", or "thorough"
- The target has never been Trinity'd before AND is >500 LOC

### Quick Trinity Flow
```
Phase 0: Scope + Load Context (same as full)
Phase 1: devTeam DIAGNOSES (same as full)
  └── IF ≤3 gaps AND all LOW/MED → QUICK MODE CONFIRMED
  └── IF >3 gaps OR any CRIT → AUTO-ESCALATE to Full Trinity
Phase Q: IMPLEMENT DIRECTLY (skip profTeam)
  └── Apply fixes based on devTeam's gap descriptions + existing knowledge
  └── Use project docs, existing research, shared learnings — no new research
Phase 4: devTeam RE-SCORES (same as full)
Phase 6: Quick Report (abbreviated)
Phase 7: Persist Learnings (same as full)
```

### Quick Trinity Report Format
```
QUICK TRINITY — REPORT
═══════════════════════
Target: [name] | Mode: QUICK (≤3 gaps, all LOW/MED)
Score: [before]/35 → [after]/35 (+[delta]) | Grade: [X] → [Y]
Gaps Fixed: [list]
Regressions: [none / details]
Runtime: ~[X] minutes (vs ~[Y] minutes estimated for full)
```

### Auto-Escalation
If during Phase Q implementation, the fix turns out to be more complex than expected:
1. Stop implementing
2. Report: "Quick Trinity escalating to Full — gap [X] requires research."
3. Continue from Phase 2 (profTeam) with the gap as a targeted research question
4. No re-diagnosis needed — Phase 1 scores are still valid

---

**Incremental checkpoints**: Follow _shared_protocols.md SS5. Write at every phase boundary (see Phase table below the workflow).

---

**Session safety**: Follow _shared_protocols.md SS6.

---

## Workflow

### Phase 0: Scope, Detect & Load Context

1. **Read `_learnings.md`** — accumulated insights from previous Trinity runs
2. **Read `.claude/shared/_shared_learnings.md`** — cross-skill learnings
3. **Parse the target**: What system/skill/architecture is being improved?
4. **Auto-detect target type** using preset library (see Target Type Auto-Presets)
5. **Load scoring dimensions** from the matched preset
6. **Cross-run check**: Search `_learnings.md` for previous runs on this same target
   - If found: load previous final scores as historical baseline
   - Report: "This target was last Trinity'd on [date]. Previous final score: [X/35]. Starting from there."
   - If not found: "First Trinity run on this target."
7. **Set baseline**: Read relevant files, existing scores, known issues
8. **project docs Reference Mandate (v3.0)**: If target domain is **Code/Architecture**, **Game Design**, or **Skill/Tool** AND project is your project — load the relevant project docs(s) BEFORE beginning diagnosis. Use parallel Read calls. Per SL-004 (HIGH confidence, 7+ runs): project docs provide 90%+ of needed context and outperform web searches for UE5/project topics. project docs content injects into Phase 1 diagnosis and Phase 2 research targets. Skip web searches that project documentation already answers.
   - Code/Architecture target → load project reference docs + domain chapter
   - Combat/Weapons target → load project reference docs
   - AI target → load project reference docs
   - UI target → load project reference docs
   - Space/Traversal target → load project reference docs
   - Performance target → load project reference docs + Ch.13
9. **Inform user**: "Holy Trinity v3.0 deploying on [target]. Type: [preset]. Dimensions: [list]. Parallel execution active. project docs pre-loaded: [chapters]. Starting with diagnosis."

### Phase 1: devTeam v4.0 DIAGNOSES (Pass N)

Deploy devTeam v4.0 analysis on the target:

1. **Read all relevant files** — source code, SKILL.md, docs, configs
2. **Score every dimension** using devTeam v4.0's calibrated methodology:
   - 7 dimensions (from preset) scored 0-5 each
   - Calibrated weights from devTeam's accumulated data
   - Anti-pattern detection (domain-specific)
   - Complexity metrics (CC, CBO, LOC if code target)
3. **Tag protected dimensions**: Any dimension scoring ≥4/5 is PROTECTED
4. **Rank all gaps by impact** — highest-impact issues first
5. **Generate research targets** — specific questions for profTeam, derived from gaps

#### Diagnostic Report Format
```
HOLY TRINITY v4.0 — DIAGNOSTIC REPORT (Pass [N])
══════════════════════════════════════════════════

Target: [name]
Type: [auto-detected preset]
Domain: [detected domain]
Cross-Run: [first run / previous: X/35 on DATE]

DIMENSION SCORES (calibrated weights):
| # | Dimension | Score | Weight | Weighted | Status |
|---|-----------|-------|--------|----------|--------|
| 1 | [dim]     | X/5   | ×W     | X.X      | PROTECTED / GAP / OK |
...
| TOTAL | | X/35 | | X.X/35 | Grade: [A-F] |

PROTECTED DIMENSIONS (must not regress):
  ✓ [dim] — [score]/5 — [why it's strong]

TOP GAPS (ranked by weighted impact):
  1. [GAP] — Weighted impact: [X.X points] — Severity: [CRIT/HIGH/MED]
  2. [GAP] — Weighted impact: [X.X points] — Severity: [CRIT/HIGH/MED]
  3. [GAP] — Weighted impact: [X.X points] — Severity: [CRIT/HIGH/MED]

ANTI-PATTERNS FOUND:
  • [pattern] — [where] — [severity] — [domain-specific?]

WHAT'S WORKING (preserve these):
  • [strength] — [evidence]

RESEARCH TARGETS FOR profTeam v4.0:
  → [specific question 1 from Gap 1]
  → [specific question 2 from Gap 2]
  → [specific question 3 from Gap 3]

VELOCITY (if Pass ≥2):
  Pass [N-1] → [N]: [delta] points | Velocity: [rate]
  Trend: [accelerating / steady / decelerating / stalled]
```

6. **Present to user** — User sees scores and gap list. They may steer priorities.

### Phase 2: profTeam v4.0 RESEARCHES (Targeted)

Deploy profTeam v4.0 with TARGETED prompts from the diagnostic:

1. **Research targets come from devTeam v4.0** — NOT broad topic research
2. **Topic classification**: profTeam auto-classifies based on the gap descriptions
3. **Agent config from ROI data**: profTeam selects optimal agents from accumulated learnings
4. **Agent D (Pitfalls) always deployed** — proven highest ROI across all runs
5. **Agent E (Codebase) mandatory** if target is existing code
6. **Smart Cycle compression active** — profTeam decides 1-3 passes based on consensus strength
7. **Checkpoint protocol active** — all agents write results to disk
8. **Output per agent**: Specific fix recommendations with:
   - What to change (file, section, specific edit)
   - Why it fixes the gap (traced back to devTeam's dimension score)
   - Evidence it works (source tier, shipped examples)
   - Risk if applied incorrectly
   - **Regression risk assessment**: Could this fix break a protected dimension?

### Phase 2.5: Verifiable Data Gate (v3.0)

**MANDATORY CHECKPOINT** — No fix proceeds to implementation without passing this gate. This is a hard blocker, not advisory.

For every proposed fix from Phase 2 research:

1. **Source Tier Check**: What is the strongest source backing this fix?
   - T1 (Official docs, API reference, framework maintainers) ✓
   - T2 (GDC talks, AAA studio postmortems, named practitioners) ✓
   - T3 (Peer-reviewed academic papers, ACM/IEEE) ✓
   - T4 (Engine/framework source code analysis) — needs T1-T3 corroboration
   - T5 (Community tutorials, forums) — NEVER sufficient alone

2. **Corroboration Check**: Does the fix have ≥2 INDEPENDENT sources at T1-T3?
   - YES → **VERIFIED** — passes gate, proceeds to Phase 3
   - ONE T1-T3 source → **PROBABLE** — passes gate with [PROBABLE] tag, implement with extra care
   - T4 or T5 only → **UNVERIFIED** — **BLOCKED**. Route back to profTeam with targeted research brief.
   - **Engine-Version Exception (v3.0)**: If the topic is engine-version-specific (e.g., UE5.7 API behavior) AND T1 official docs do not cover it — then **T4 (engine source code analysis) + T2 (GDC talk or named practitioner) = VERIFIED**. Rationale: engine source is ground truth when docs lag behind. Tag as `[VERIFIED-ENGINE-SOURCE]` to distinguish from standard VERIFIED.

3. **Gate Report**:
   ```
   VERIFIABLE DATA GATE — Pass [N]
   ═══════════════════════════════
   Fix 1: [description] — T[N] × [N] sources — VERIFIED ✓ → proceeds
   Fix 2: [description] — T[N] × 1 source — PROBABLE → proceeds [PROBABLE]
   Fix 3: [description] — T5 only — UNVERIFIED → BLOCKED, routed to profTeam
   
   Proceeding: [N] fixes | Blocked: [N] fixes
   ```

4. **Additive Upgrade Guard** (v3.0 — applies when target is Skill/Tool):
   When Holy Trinity is improving a skill file (SKILL.md, `_learnings.md`, or any `.claude/` file):
   - **ZERO REMOVALS** without explicit user approval
   - Every change is an additive layer — new sections, new steps, new rules added ON TOP of existing content
   - Existing content is preserved verbatim unless it is factually incorrect
   - Restructuring (moving existing content) requires user approval
   - If a fix requires removing content: present it as `[FLAG: REMOVAL NEEDED]` and ask user before proceeding
   - This guard exists because skill files contain accumulated knowledge — removing any section could erase validated learnings

---

### Phase 3: IMPLEMENT (with Regression Guard)

Apply researched solutions as concrete changes:

#### Independence Analysis (v2.0)
Before implementing, classify fixes:
- **Independent fixes**: Touch different files/systems, no shared state → implement in PARALLEL
- **Dependent fixes**: Fix B relies on Fix A's changes → implement SEQUENTIALLY
- **Conflicting fixes**: Two fixes modify the same code differently → implement the higher-impact one first, re-evaluate the other

#### Gap Clustering (v2.1 — Efficiency → 5/5)

Before implementing, analyze gaps for compound fix opportunities:

1. **Cluster related gaps**: Group gaps that share the same root cause or can be fixed with a single change
   - E.g., "Missing data contract" + "Inappropriate intimacy" in the same module → one refactor fixes both
   - E.g., "Stale learnings" + "Missing cross-skill propagation" → one learnings protocol update fixes both
2. **Compound fix scoring**: A single change that resolves 2+ gaps gets priority
   - Report: "Gap cluster found: Gaps [N, M] share root cause [X]. Single fix resolves both."
3. **Avoid over-clustering**: Only cluster if the compound fix is cleaner than separate fixes

#### Implementation Protocol
For each fix (parallel when independent, clustered when compound):
1. **Pre-fix snapshot**: Record all current dimension scores
2. **Apply the change** (Edit/Write tool)
3. **Implementation verification** (v2.1 — see below)
4. **Quick regression check**: Does this change plausibly affect any protected dimension?
   - If yes → verify immediately before proceeding
   - If no → proceed, verify in Phase 4
5. **Log the change**:
   ```
   IMPLEMENTATION LOG (Pass [N]):
   • [file] — [what changed] — fixes Gap [N] — regression risk: [LOW/MED/HIGH]
   • [file] — [compound fix] — fixes Gaps [N, M] — cluster: [root cause]
   ```

#### Implementation Verification (v2.1 — Reliability → 5/5)

After EVERY file modification, verify the change is valid:

**For code files (.h, .cpp, .ts, .tsx, .py):**
- Re-read the modified file to confirm the edit was applied correctly
- Verify no syntax was broken (matching braces, no dangling imports)
- If the project has a build command: run it to catch compile errors
- If the project has tests: run relevant tests

**For skill files (SKILL.md, _learnings.md):**
- Re-read the file to confirm structure is intact
- Verify markdown formatting (headers, tables, code blocks)
- Check that all cross-references still point to valid sections

**For config files (.json, .md settings):**
- Verify JSON is valid (no trailing commas, matching brackets)
- Verify referenced paths/files exist

**If verification fails:**
- Rollback the specific change
- Log: "Implementation verification failed: [what broke]. Rolled back."
- Try alternative approach or escalate to user

#### Escalation Protocol (v2.0)
If a fix causes a regression:
1. **Detect**: Protected dimension dropped by ≥1 point after the fix
2. **Assess severity**:
   - Fix gained [X] points on target gap
   - Fix lost [Y] points on protected dimension
   - Net: +[X-Y] or -[Y-X]
3. **Decision**:
   - If net positive AND regression < 1 point → ACCEPT with warning
   - If net negative → ROLLBACK immediately
   - If net neutral → Present to user: "This fix improves [gap] but regresses [protected]. Your call."
4. **Reclassify**: If rollback, mark the gap as "architectural" — needs redesign, not a patch
5. **Do NOT count architectural gaps toward convergence** — they need a different approach

### Phase 4: devTeam v4.0 RE-SCORES

Run devTeam v4.0 analysis again on the modified system:

1. **Score all dimensions** — same methodology, same calibration
2. **Regression check**: Compare every dimension to the pre-implementation snapshot
3. **Compute velocity**:
   ```
   velocity[N] = (score[N] - score[N-1]) / 1  // points per pass

   velocity_trend = velocity[N] vs velocity[N-1]:
     accelerating: velocity[N] > velocity[N-1]
     steady: velocity[N] ≈ velocity[N-1] (within 1 point)
     decelerating: velocity[N] < velocity[N-1]
     stalled: velocity[N] ≤ 0
   ```

#### Re-Score Report Format
```
HOLY TRINITY v4.0 — RE-SCORE (Pass [N-1] → Pass [N])
══════════════════════════════════════════════════════

SCORE CHANGE: [old]/35 → [new]/35 (+[delta])

DIMENSION BREAKDOWN:
| Dimension | Before | After | Delta | Status |
|-----------|--------|-------|-------|--------|
| [dim]     | X/5    | Y/5   | +/-Z  | IMPROVED / STABLE / REGRESSED |

GAPS RESOLVED:
  ✓ [gap] — was [severity], now FIXED — +[X] points

GAPS REMAINING:
  ✗ [gap] — still [severity] — [actionable / architectural]

REGRESSIONS:
  [none / ⚠ [dim] dropped X → Y — caused by [fix] — [accepted/rolled back]]

NEW ISSUES FOUND:
  [none / ! [issue] — introduced by [fix] — [severity]]

VELOCITY: [X] points/pass | Trend: [accelerating/steady/decelerating/stalled]

CONVERGENCE STATUS: [CONTINUE / STOP — reason]
```

### Phase 5: Convergence Decision (v2.0 — Velocity-Aware)

#### CONTINUE if ALL true:
- Score improved by ≥2 points since last pass
- Velocity is not stalled (velocity > 0)
- At least 1 remaining gap is actionable (not architectural)
- No unresolved regressions on protected dimensions
- User hasn't signaled to stop

#### STOP if ANY true:
- Score improved by <2 points (diminishing returns)
- Velocity has been decelerating for 2+ consecutive passes AND current delta <3
- All remaining gaps are architectural (require redesign, not patches)
- Score hit target threshold (if user set one)
- Unresolved regression that user chose not to accept
- User signals to stop
- **5 passes completed** (hard cap — prevents infinite loops)

#### ESCALATE if:
- A critical gap exists but every attempted fix causes regression
- Two fixes conflict (both needed but mutually exclusive)
- → Present the architectural dilemma to the user with options

### Convergence Prediction (v4.0 — Data-Driven Model)

Holy Trinity now has concrete convergence data from 13+ runs. Use this table as the prediction model:

#### Convergence Reference Table (computed from _learnings.md)

| Target Type | Runs | Avg Passes | Avg Delta/Pass | Typical Pattern | Predicted Range | Hard Cap |
|-------------|------|-----------|----------------|-----------------|-----------------|----------|
| **Code/Architecture** | 3 | 1.3 | +10.2 | Fast start, single pass for well-scoped targets | 1-2 passes | 3 |
| **Skill/Tool** | 2 | 1.5 | +11.0 | Implementation gaps close in 1 pass | 1-2 passes | 3 |
| **Standalone Tool** | 4 | 1.25 | +7.0 | Fast start, decelerating — exhausts actionable gaps in 1-2 | 1-2 passes | 3 |
| **Game Design** | 1 | 2.0 | +4.5 | Creative gaps need research pass | 2-3 passes | 4 |
| **Product/Business** | 1 | 1.0 | +2.7 | Validation-focused, one pass sufficient | 1 pass | 2 |
| **Infrastructure** | 1 | 3.0 | +8.3 | Greenfield massive gains, decelerating | 2-3 passes | 4 |
| **Research KB** | 1 | 1.0 | N/A | Single-pass, no scoring loop | 1 pass | 1 |

#### Prediction Protocol
1. **Look up target type** in the reference table
2. **Adjust for target state**:
   - Greenfield (no existing code/content) → add +1 pass to predicted range
   - Previously Trinity'd target → use previous final score as baseline, predict fewer passes
   - Small target (<500 LOC or single file) → clamp to 1 pass (Quick Trinity candidate)
3. **Report at Phase 0**: "Convergence prediction: [X] passes (±1). Based on [N] previous [type] runs averaging [Y] passes with [Z] pts/pass."
4. **Set dynamic hard cap** from table (NOT always 5)

#### Prediction Accuracy Tracking (v4.0)
After EVERY run, compare prediction to actual:
```
### Prediction Accuracy: [Target] — [Date]
- Predicted: [X] passes | Actual: [Y] passes | Error: [±Z]
- Predicted delta: [X] pts | Actual delta: [Y] pts | Error: [±Z]
- Table update needed: [Yes — adjust [type] avg / No — within ±1]
```

When prediction error > ±1 pass for a target type across 2+ runs → update the reference table averages. The table is a LIVING model, not static.

#### Calibration Echo — Convergence Prediction (v2.1 per SL-062)

Close the self-improvement loop: track whether Holy Trinity's convergence prediction (Phase 0 lookup) matches actual runs, then auto-adjust the reference table. Mirrors devTeam v4.0 Calibration Echo pattern.

**Protocol**:
1. **Before starting passes**: record predicted pass count + predicted final score from Phase 0 lookup
2. **After convergence**: record actual pass count + actual final score
3. **Compute accuracy**: `prediction_accuracy = 1 - (|predicted - actual| / max(predicted, actual))`
4. **Write IMMEDIATELY per §5** to `_learnings.md`:
   ```
   ### Calibration Echo: Convergence — [Target] — [Date]
   <!-- meta: { "run_id": "trinity_echo_[target]_[date]", "domain": "skills", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "staleness_check": "[date]" } -->
   - Predicted: [X] passes, [Y] final pts | Actual: [Z] passes, [W] final pts
   - Accuracy: [N]% | Status: WELL-CALIBRATED (>66%) | DEVELOPING (33-66%) | MISCALIBRATED (<33%)
   - Adjustment: [none / adjust [target type] avg passes ±N / adjust avg delta ±M]
   ```
5. **After 3+ echo events** on same target type, re-sum averages and update the reference table. Refresh `staleness_check` per §11.

This closes the loop across Trinity runs. Convergence predictions get smarter with every run. Over 10+ runs per target type, Trinity develops target-specific expertise that drives automatic pass-count planning.

#### Cross-Target Pattern Matching (v4.0)

When a gap pattern matches one seen in a DIFFERENT target:
1. **Search _learnings.md** for similar gap descriptions across all past runs
2. **If match found**: Load the solution that worked for that gap
3. **Cross-pollinate**: "Gap [X] matches pattern from [previous target]. Solution there was [Y]. Applying adapted version."
4. **Track cross-target transfers**: Log which solutions transferred successfully vs. needed adaptation
5. **Build pattern library**: After 5+ successful cross-target transfers, promote the pattern to `_shared_learnings.md`

This enables Trinity to solve problems FASTER on new targets by recognizing patterns it's seen before, even in different domains.

When stopping, produce the **Final Trinity Report**.

### Phase 6: Final Trinity Report (v2.0)

```
HOLY TRINITY v4.0 — FINAL REPORT
══════════════════════════════════

Target: [name]
Type: [preset]
Passes: [N]
Runtime: [approximate]

SCORE EVOLUTION:
  Pass 0: [X]/35 (baseline)      | Velocity: —
  Pass 1: [Y]/35 (+[delta])      | Velocity: [V1]
  Pass 2: [Z]/35 (+[delta])      | Velocity: [V2] ([trend])
  ...
  Final:  [F]/35 — Grade: [A-F]  | Avg velocity: [V_avg]

CROSS-RUN COMPARISON (if previous runs exist):
  Previous final: [X]/35 on [date]
  Current final:  [Y]/35
  Cross-run delta: +[Z] points
  Overall trend: [improving / stable / declining]

TOTAL IMPROVEMENT: +[total delta] points across [N] passes

CHANGES MADE:
  [N] files modified
  [N] gaps resolved (of [M] identified)
  [N] parallel implementations
  [N] regressions caught and handled

GAPS RESOLVED:
  ✓ [gap] — resolution — score impact — pass resolved

PROTECTED DIMENSIONS (final status):
  ✓ [dim] — maintained at [X]/5 throughout
  ⚠ [dim] — briefly regressed in Pass [N], recovered in Pass [N+1]

REMAINING GAPS:
  ✗ [gap] — classification: [actionable/architectural] — recommended approach

REGRESSIONS HANDLED:
  [count] detected | [count] rolled back | [count] accepted | [count] escalated

ESCALATIONS:
  [none / architectural dilemmas presented to user]

SHARED LEARNINGS GENERATED:
  [SL-NNN] — [description] — applies to: [skills]

CONVERGENCE REASON: [diminishing returns / velocity stall / all resolved / architectural limit / user stop / hard cap]
```

### Phase 7: Persist Learnings (v3.1 — Consolidation)

**NOTE**: By this phase, checkpoint learnings from Phases 1-4 should ALREADY be written (see Incremental Learning Protocol above). Phase 7 consolidates them into the full structured entry.

1. **Consolidate checkpoint entries** — merge Phase 1-4 checkpoint learnings into one structured entry (see format in MANDATORY section below)
2. **Append consolidated entry to `_learnings.md`** with full run details + velocity data + regression events
3. **Write any remaining shared learnings** to `.claude/shared/_shared_learnings.md` — per SL-043: grep max ID first
4. **Update `.claude/shared/skill_dependency_graph.md`** if data contracts changed
5. **Update `.claude/shared/bifrost_api_contract.md`** if BifrostPDF patterns discovered
6. **If cross-run data exists**: Update the trend analysis for this target
7. **Verify checkpoint learnings exist** — if Phases 1-4 checkpoints are missing (compaction ate them), reconstruct from memory and write the full entry anyway

## Scoring
35-point scale (7 dimensions x 5). Grades: A=30-35, B=25-29, C=18-24, D=12-17, F=<12. DevTeam v3.0 calibration engine applies across all target types.

## Cross-Run Intelligence (v2.0)

The Holy Trinity maintains a **target history** in `_learnings.md`. Key capabilities:

1. **Score continuity**: When re-running on the same target, the baseline is the PREVIOUS run's final score, not a fresh diagnosis. This shows long-term improvement.

2. **Gap memory**: If a gap was marked "architectural" in a previous run, don't re-attempt the same patches. Instead:
   - Report: "Gap [X] was classified as architectural in [previous run date]"
   - Research redesign approaches instead of patches

3. **Calibration transfer**: If devTeam calibrated its weights during a previous run on this target type, load those weights as the starting calibration.

4. **Diminishing returns prediction**: After 3+ runs on the same target, compute the average velocity per pass across all runs. Predict how many passes are likely productive.

5. **Cross-target learning**: If a solution worked on one target type, check if similar solutions apply to other targets with the same gap pattern.

## Multi-Target Batch Mode (v3.2)

When Trinity is invoked on multiple targets simultaneously (e.g., "trinity on building + warp"), use batch orchestration:

### Batch Flow
1. **Classify targets**: Are they independent systems or coupled?
2. **Independent targets**: Run Phase 0-1 (scope + diagnosis) on ALL targets in parallel using Explore agents
3. **Merge diagnosis**: Present a unified triage table:
   ```
   MULTI-TARGET DIAGNOSIS
   ═══════════════════════
   | Target | Score | Top Gap | Severity | Coupled? |
   |--------|-------|---------|----------|----------|
   | [A]    | X/35  | [gap]   | CRIT     | No       |
   | [B]    | Y/35  | [gap]   | HIGH     | Yes→A    |
   ```
4. **Coupled targets**: If fixing Target A affects Target B (shared code), fix A first, then re-diagnose B
5. **Independent targets**: Phase 2-3 (research + implement) runs in parallel
6. **Unified Phase 4**: Re-score all targets in one pass
7. **Single Final Report**: Combined report showing all targets

### When to Auto-Batch
- User mentions 2+ systems in one request
- devTeam diagnosis reveals cross-system gaps (Gap in A caused by B)
- Godspeed mode + multiple items = auto-batch (don't ask)

### Batch vs Sequential Decision
| Condition | Mode |
|-----------|------|
| Targets share no files | Parallel batch |
| Targets share <3 files | Parallel batch with merge check |
| Targets share >3 files | Sequential (A→B) to avoid conflicts |
| One target blocks another | Sequential, blocking target first |

## Godspeed Integration (v3.2)

When godspeed mode is active during Trinity:
- **Skip user confirmation steps** — auto-proceed at every phase boundary
- **Quick Trinity is the default** unless gaps are CRITICAL or >3
- **Triage protocol from Godspeed takes priority** for ordering multi-target work
- **Context-burn awareness applies** — use Explore agents for diagnosis, keep main context lean
- **Output format**: Use Godspeed's terse `✓/✗` style for phase completions, not full report blocks between phases. Full report only at end.

## Sub-Skill Data Contracts (v4.0 — Parseable Schemas)

The interfaces between Trinity, devTeam, and profTeam are defined as structured contracts. Downstream skills validate against these schemas.

### devTeam → Trinity Output Contract
```json
{
  "target": "string — system/file name",
  "domain": "string — auto-detected domain",
  "dimensions": [
    { "name": "string", "score": "int 0-5", "weight": "float", "weighted": "float", "status": "PROTECTED|GAP|OK" }
  ],
  "total": "int 0-35",
  "grade": "A|B|C|D|F",
  "protected": ["string — dimension names with score ≥4"],
  "gaps": [
    { "description": "string", "severity": "CRIT|HIGH|MED|LOW", "weighted_impact": "float", "actionable": "bool" }
  ],
  "anti_patterns": [
    { "name": "string", "severity": "string", "location": "string", "domain_specific": "bool" }
  ],
  "research_targets": ["string — specific questions for profTeam"],
  "calibration": { "data_points": "int", "weights": {"Law_1": "float", "Law_2": "float"} }
}
```

### Trinity → profTeam Input Contract
```json
{
  "research_targets": ["string — from devTeam gaps, NOT broad topics"],
  "topic_classification": "string — auto-classified from gap descriptions",
  "context": { "target_files": ["string"], "bible_chapters": ["string"], "existing_research": ["string"] },
  "constraints": { "max_agents": "int", "agent_d_mandatory": true, "agent_e_mandatory": "bool — true if existing code" }
}
```

### profTeam → Trinity Output Contract
```json
{
  "fixes": [
    {
      "gap_ref": "string — which devTeam gap this fixes",
      "description": "string",
      "file": "string", "section": "string", "edit": "string",
      "source_tier": "T1|T2|T3|T4|T5",
      "corroboration_count": "int",
      "verification_status": "VERIFIED|PROBABLE|UNVERIFIED",
      "regression_risk": "LOW|MED|HIGH",
      "regression_dims": ["string — which protected dims could be affected"]
    }
  ],
  "confidence_matrix": { "verified": "int", "probable": "int", "unverified": "int", "contradicted": "int" },
  "compression_decision": "COMPRESS|PARTIAL|FULL"
}
```

**Validation**: At each phase boundary, Trinity checks that the actual output matches the contract structure. Missing required fields → warning logged. Malformed structure → flag and proceed with best-effort parsing.

## Historical Data Compression (v4.0 — Efficiency)

_learnings.md grows with every run. Without compression, Phase 0 loading burns excessive context.

### Rolling Window Protocol
1. **Active window**: Last 10 runs per target type — load in full detail
2. **Archive window**: Runs 11+ — compress to summary format:
   ```
   ### Archived: [Target] — [Date] — Score: [X]→[Y] (+[Z]) — Grade: [G] — Passes: [N]
   Key findings: [1-2 sentences]
   ```
3. **Aggregate data survives**: Convergence Reference Table, ROI leaderboards, calibration weights — these are computed from all runs (including archived) and stored as aggregates, not individual entries
4. **Archive trigger**: When _learnings.md exceeds 500 lines, archive oldest runs beyond the 10-run window
5. **Archive location**: Bottom of _learnings.md under `## Archived Runs` section
6. **Recovery**: If a specific archived run's details are needed, they can be reconstructed from checkpoint files (if available) or from the aggregate data

### What NEVER gets archived:
- Convergence Reference Table (living model)
- Cross-Run Target History (score trajectories)
- Any run flagged as "breakthrough" or "critical discovery"

## Dry-Run Mode (v4.0 — Configuration Validation)

Quick validation of Trinity configuration without executing changes.

### When to Use
- User says "trinity dry-run", "dry run on [target]", "test trinity config"
- Before a full Trinity run on a new target type to verify preset detection
- When debugging Trinity configuration issues

### Dry-Run Flow
```
Phase 0: Scope + Load Context (FULL — same as real run)
Phase 0.5: DRY-RUN VALIDATION
  1. Report: target type detected, preset loaded, dimensions selected
  2. Report: calibration data available ([N] previous reviews, weights)
  3. Report: convergence prediction ([X] passes based on [N] historical runs)
  4. Report: files that WOULD be read (Critical + High priority list)
  5. Report: profTeam agent config that WOULD be deployed
  6. Report: project docs / existing research that WOULD be loaded
  7. Report: estimated context cost (files × avg lines)
  → STOP. No scoring, no research, no implementation.
```

### Dry-Run Output
```
HOLY TRINITY v4.0 — DRY RUN
════════════════════════════
Target: [name] | Type: [detected preset] | Domain: [domain]
Dimensions: [7 dimension names]
Calibration: [N] data points | Weights: [list]
Convergence prediction: [X] passes (±1)
Files to scan: [N] Critical, [M] High, [K] Medium
ProfTeam config: [N] agents ([list])
Context estimate: ~[X]K tokens for Phase 0-1
Previous runs: [N] on this target, last: [date] at [score]/35
STATUS: CONFIG VALID — ready for full run
```

## Protocols

Follow `${CLAUDE_PLUGIN_ROOT}/shared/_shared_protocols.md` for: pre-work loading, source tiers, parallel execution, post-invocation learning, incremental checkpoints, session safety, additive upgrade discipline.
