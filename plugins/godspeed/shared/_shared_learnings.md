# Shared Learnings Registry
<!-- Last aggregation: 2026-04-10 -->
<!-- Total entries: 49 | Active: 49 | Quarantined: 0 | Archived: 0 -->
<!-- NOTE: SL-033 to SL-037 were renumbered on 2026-04-02 to fix duplicate IDs. Original SL-033/034/035 (v3.0 upgrades) retained. Duplicates became SL-038/039/040. SL-036/037 became SL-041/042. -->
<!-- 2026-04-09: SL-049/050/051 added via ecosystem audit cross-skill promotion (your-automation-skill → UE5 AnimGraph, project-init → Pascal FP32, project-init → NF4 bf16 leak) -->
<!-- 2026-04-10: SL-075/076/077 added via close-session cross-promotion from author skill (verify-at-source methodology, JSON manifest drift detection, directory rename escalation pattern). Highest existing SL-ID was SL-074. Next available: SL-078 -->
<!-- DOMAIN SPLIT (2026-04-07): UE5/your project entries (SL-019 to SL-028, SL-030-032, SL-038-042) moved to _shared_learnings_ue5.md. Load that file only for UE5 projects. -->

## Cross-Skill Methodology (added 2026-04-10 from author skill build)

### [SL-075] Verify at source, never at summary
- **Source skill**: author
- **Applies to**: ALL (universal methodology)
- **Confidence**: HIGH (1 load-bearing incident, catastrophic blast radius when violated)
- **Last validated**: 2026-04-10
- **Detail**: Never propagate metadata from a secondary source without opening the primary. During author skill build, "~2,716 project docs pages" was misread from Roadmap's total-docs stat as project documentation PDF's single-file page count, which led to B_bible.md claiming B:7 was at pages "~181-220" when project documentation is actually 36 pages total. The error was caught only by a verification test that errored on `pdftoppm first page (181) can not be after last page (36)`. Opening a PDF to verify costs ~3 seconds + 1K tokens. The cost of propagating a wrong number is the whole system's correctness score.
- **Action**: When writing any index, manifest, or metadata file that references another source, OPEN the primary source and verify the stat before writing it down. Never trust a stat that comes through an intermediate document — go one level deeper.
- **Applies to skills that write structured metadata**: author, blueprint, cycle, devTeam, profTeam, holy-trinity, reference, organizer, scanner.

### [SL-076] JSON manifest + portable validator beats regex-on-markdown for drift detection
- **Source skill**: author
- **Applies to**: ALL skills with structured ground-truth data
- **Confidence**: HIGH (62/63 PASS on first run proved the pattern; dedupe logic cut 160+ references to 17 unique checks)
- **Last validated**: 2026-04-10
- **Detail**: When a skill has machine-verifiable ground truth (file paths, line counts, PDF page counts, tool references), store it in a JSON manifest (not free-form markdown). Write a zero-dep validator that (1) auto-detects its own skill directory via `Path(__file__).resolve().parent` for rename portability, (2) dedupes references before checking, (3) uses regex for PDF page counting to avoid pypdf dependency, (4) reports WARN vs FAIL for conceptual vs required entries. Markdown files can then mirror the JSON for human readability without being the source of truth.
- **Evidence**: `author/validator_manifest.json` + `author/toolsets.json` + `validate_author.py` — 63 checks run in <1 second, caught your-3d-skill as a known gap without blocking, survived the knowledge-router → author rename with zero edits to the validator script.
- **Action**: For any new skill with structured data: ship a JSON manifest + a portable validator + a README section that names the validator command. Do NOT regex-parse markdown for drift detection.
- **Applies to skills**: author, reference, organizer, find, close-session (for session_log.json), init variants.

### [SL-077] Directory rename on Windows can hit busy locks — use cp + deregister
- **Source skill**: author + godspeed (escalation event)
- **Applies to**: ALL skills doing dir-level renames
- **Confidence**: MEDIUM (1 event, but the error message was unambiguous and the workaround is documented)
- **Last validated**: 2026-04-10
- **Detail**: `mv ~/.claude/skills/knowledge-router ~/.claude/skills/author` failed with "Device or resource busy" — the directory was held open by the skill registry watcher. Safer pattern: (1) `cp -r old_dir/. new_dir/` to duplicate contents, (2) rename the old `SKILL.md` to `SKILL_DEPRECATED.md` to deregister the old skill from the registry, (3) leave the old dir as historical archive (do NOT rm without explicit consent per Sacred Rule #2). This pattern preserves Sacred Rule #2 (never delete without consent) while achieving the rename.
- **Evidence**: godspeed `_learnings.md` documented this as an L1 escalation. Old `knowledge-router/` dir now exists with `SKILL_DEPRECATED.md` and is invisible to the skill registry. New `author/` dir is fully registered and functional.
- **Action**: When renaming a skill directory, use cp + deregister rather than mv. Add `directory_rename` to the godspeed Problem Class Routing Table with optimal start level = L1 (known workaround exists).
- **Applies to skills**: godspeed, organizer, any skill that manages skill directories.

## API & Tool Patterns

### [SL-001] BifrostPDF: use `code()` not `code_block()`
- **Source skill**: cycle
- **Confirmed by**: blueprint, profTeam, professor
- **Applies to**: ALL PDF-generating skills
- **Confidence**: HIGH (3+ Cycle runs verified)
- **Last validated**: 2026-03-21
- **Detail**: `code_block()` does not exist. The correct method is `code(lines=[], title=None, line_numbers=False)`.

### [SL-002] BifrostPDF: use `gold_box()` / `cyan_box()` not `callout()` or `callout_box()`
- **Source skill**: cycle
- **Confirmed by**: blueprint, profTeam
- **Applies to**: ALL PDF-generating skills
- **Confidence**: HIGH (3+ Cycle runs verified)
- **Last validated**: 2026-03-21
- **Detail**: There is no `callout()` or `callout_box()` method. Use `gold_box(title, lines=[])`, `cyan_box()`, `magenta_box()`, `green_box()`, `red_box()`.

### [SL-003] BifrostPDF: use `code_highlighted()` for syntax-colored code
- **Source skill**: blueprint
- **Confirmed by**: cycle
- **Applies to**: ALL PDF-generating skills
- **Confidence**: HIGH
- **Last validated**: 2026-03-21
- **Detail**: `code_highlighted(lines=[], title=None, lang="cpp")` provides syntax coloring. Use instead of `code()` when language-specific highlighting is desired.

## Research Patterns

### [SL-004] project docs outperform web searches for UE5/project context
- **Source skill**: cycle
- **Confirmed by**: profTeam, blueprint
- **Applies to**: blueprint, professor, profTeam, cycle
- **Confidence**: HIGH (90%+ content available from project docs before web search in 7 Cycle runs)
- **Last validated**: 2026-03-21
- **Detail**: Always read the relevant project docs BEFORE conducting web searches. project docs provides 90%+ of needed architectural context. Web searches only needed for gaps.

### [SL-005] Existing Research PDFs are #1 most valuable source
- **Source skill**: cycle
- **Confirmed by**: profTeam
- **Applies to**: blueprint, professor, profTeam, cycle
- **Confidence**: HIGH (validated across 7 Cycle runs)
- **Last validated**: 2026-03-21
- **Detail**: Check `Docs/Design Systems/Research/` FIRST before any web research. Existing PDFs covered 80-90% of content in multiple runs.

### [SL-006] Pre-gathered context eliminates Cycle 1 inventory time
- **Source skill**: cycle
- **Confirmed by**: profTeam
- **Applies to**: cycle, profTeam
- **Confidence**: HIGH (validated in 5+ runs)
- **Last validated**: 2026-03-21
- **Detail**: Running parallel scan agents (Explore, Grep) BEFORE starting Cycle cuts Phase 1 time dramatically. All code + docs should be gathered before Cycle begins.

## Operational Patterns

### [SL-007] For God Class files (>1000 LOC): use chunked reads
- **Source skill**: cycle
- **Confirmed by**: profTeam
- **Applies to**: ALL skills reading source code
- **Confidence**: HIGH
- **Last validated**: 2026-03-21
- **Detail**: Files >1000 lines hit 25K token limit. Use `offset` and `limit` parameters (200 lines per chunk) with parallel Read calls.

### [SL-008] C++ solutions always preferred over editor/Blueprint wiring
- **Source skill**: devTeam
- **Confirmed by**: cycle, blueprint
- **Applies to**: ALL skills proposing implementations
- **Confidence**: HIGH (user feedback)
- **Last validated**: 2026-03-21
- **Detail**: User preference — minimize Blueprint/editor wiring. All proposed implementations must be C++ first with UPROPERTY/UFUNCTION exposure.

### [SL-009] Mechanical changes are permanent — never revert without explicit request
- **Source skill**: devTeam
- **Confirmed by**: N/A (user directive)
- **Applies to**: ALL skills
- **Confidence**: HIGH (direct user feedback)
- **Last validated**: 2026-03-21
- **Detail**: Once gameplay mechanics are implemented and accepted, they are permanent. Never revert or undo mechanics unless the user explicitly requests it.

### [SL-010] Agent D (Edge Cases/Pitfalls) consistently highest-value in profTeam
- **Source skill**: profTeam
- **Confirmed by**: N/A (4/5 runs confirmed)
- **Applies to**: profTeam
- **Confidence**: HIGH
- **Last validated**: 2026-03-21
- **Detail**: The Pitfalls/Edge Cases agent finds the most actionable insights. Always deploy. Agent E (Codebase-specific) is second most valuable for debugging topics.

### [SL-011] DevTeam gate should run AFTER cross-reference, not before
- **Source skill**: profTeam
- **Confirmed by**: N/A (Weapon Architecture run validated)
- **Applies to**: profTeam
- **Confidence**: MEDIUM
- **Last validated**: 2026-03-18
- **Detail**: Running devTeam validation after cross-referencing agent findings (not during) catches more issues because it can evaluate the complete picture.

### [SL-012] Cycles 2-3 can be safely compressed when consensus is strong
- **Source skill**: profTeam
- **Confirmed by**: cycle
- **Applies to**: profTeam, cycle
- **Confidence**: HIGH (3/5 profTeam runs, 2+ Cycle runs)
- **Last validated**: 2026-03-21
- **Detail**: When agent consensus is strong (0 contradictions, 90%+ verified findings), Cycles 2-3 can be compressed into a single pass. Don't force 3 passes when 1 post-consensus pass suffices.

## v2.0 Upgrade Patterns (2026-03-25)

### [SL-013] Regression guard: tag protected dimensions at ≥4/5 before any changes
- **Source skill**: devTeam v2.0, holy-trinity v2.0
- **Confirmed by**: N/A (new v2.0 protocol)
- **Applies to**: devTeam, holy-trinity, ALL skills that modify scored systems
- **Confidence**: HIGH (derived from 5 Trinity runs where fixes sometimes broke existing strengths)
- **Last validated**: 2026-03-25
- **Detail**: Before implementing any change, snapshot current scores. Tag dimensions ≥4/5 as PROTECTED. After changes, verify no protected dimension dropped ≥1 point. If regression detected: rollback or escalate.

### [SL-014] Velocity tracking predicts diminishing returns better than absolute thresholds
- **Source skill**: holy-trinity v2.0
- **Confirmed by**: N/A (derived from analyzing 5 Trinity run convergence patterns)
- **Applies to**: holy-trinity, cycle
- **Confidence**: MEDIUM (theoretical, needs validation across more runs)
- **Last validated**: 2026-03-25
- **Detail**: Track points-per-pass as velocity. If velocity declines for 2+ consecutive passes AND current delta <3, stop — even if absolute improvement ≥2. Catches diminishing returns earlier than flat threshold.

### [SL-015] Domain auto-detection enables project-agnostic scoring
- **Source skill**: devTeam v2.0
- **Confirmed by**: holy-trinity v2.0 (5 runs across code, skills, game design, products, tools)
- **Applies to**: devTeam, holy-trinity
- **Confidence**: HIGH (validated across 5 target types in Trinity learnings)
- **Last validated**: 2026-03-25
- **Detail**: Detect target domain from files/directory, load domain-specific scoring dimensions and anti-patterns. Holy Trinity proved devTeam works on code, skills, game design, products, and tools — but ONLY with adapted dimensions per type.

### [SL-016] Topic classification drives optimal agent config in profTeam
- **Source skill**: profTeam v2.0
- **Confirmed by**: N/A (derived from 5 runs with varying agent configs)
- **Applies to**: profTeam
- **Confidence**: HIGH (pattern consistent across all 5 profTeam runs)
- **Last validated**: 2026-03-25
- **Detail**: Classify topics into types (debugging, architecture, performance, game design, product). Each type has an optimal agent count and specialization mix. Debugging MUST include Codebase agent. Performance should merge Theory+Industry. Product needs 5-6 agents.

### [SL-017] Instrument before fixing for debugging topics — 3 failed attempts = stop and instrument
- **Source skill**: profTeam
- **Confirmed by**: profTeam (Terrain Flattening run — 10+ blind fix attempts before diagnostics)
- **Applies to**: ALL skills, profTeam, holy-trinity
- **Confidence**: HIGH (learned from painful experience)
- **Last validated**: 2026-03-25
- **Detail**: When debugging, if 3+ fix attempts fail, STOP fixing and START instrumenting. Add diagnostic logging first, understand the actual data flow, THEN fix. The Terrain Flattening run proved theory-based debugging is blind without runtime data.

### [SL-018] Payment architecture research needs dedicated agent for money-handling platforms
- **Source skill**: holy-trinity
- **Confirmed by**: N/A (Commission Artist Tool Blueprint run)
- **Applies to**: profTeam, blueprint, professor
- **Confidence**: HIGH (legal/compliance risk is too high for shallow coverage)
- **Last validated**: 2026-03-25
- **Detail**: For any platform that handles money (Stripe, payments, marketplace), payment architecture MUST be a dedicated research agent. The Commission Tool run surfaced critical money transmitter legal requirements that would have been missed by shallow coverage.

<!-- SL-019 to SL-028: Moved to _shared_learnings_ue5.md (UE5/your project domain) -->
<!-- SL-029 and SL-030 retained here (universal) -->

### [SL-029] User runs 12+ concurrent projects — your project is <10% of total session volume
- **Source skill**: analyst
- **Confirmed by**: N/A (session directory scan, 2026-03-28)
- **Applies to**: ALL skills assessing user capacity or workload
- **Confidence**: HIGH (verified by file counts across all project directories)
- **Last validated**: 2026-03-28
- **Detail**: In any 10-day period, the user runs 500+ sessions across 12+ projects (your project, your-trading-project, your-study-project, AnimBPDoctor, T3, atelier, Sentinel, Your-Automation-Skill, SemperFidelis, Kashi, syncscout, forge3D). your project is the primary game project but represents <10% of total session volume. Any skill assessing cognitive load, scope management, or capacity should account for this parallel project portfolio. Context-switching across 12+ projects with different tech stacks is a significant cognitive signal.

### [SL-030] UE5 engine source reading beats web search for Slate internals
- **Source skill**: professor
- **Confirmed by**: N/A (first observation)
- **Applies to**: ALL skills debugging UE5 engine-level issues
- **Confidence**: HIGH (web returned 0 useful results; source found root cause in minutes)
- **Last validated**: 2026-03-30
- **Detail**: For Slate event routing, hit testing, DetectDrag internals, and SObjectWidget behavior — read the engine source directly (SlateApplication.cpp, SObjectWidget.cpp). Web searches only surface forum posts and high-level docs that miss implementation details. The actual code has comments, line numbers, and exact algorithms.

<!-- SL-030 stays (universal). SL-031, SL-032: Moved to _shared_learnings_ue5.md -->

## v3.0 Pipeline Upgrades (2026-04-02)

### [SL-033] Parallel agent dispatch requires single-message multi-call — never sequential
- **Source skill**: holy-trinity v3.0, profTeam v3.0
- **Confirmed by**: Claude Code architecture (Agent tool accepts multiple simultaneous calls in one message)
- **Applies to**: holy-trinity, profTeam, ALL skills deploying multiple agents
- **Confidence**: HIGH (architectural fact — single-message multi-call is Claude Code's parallel execution mechanism)
- **Last validated**: 2026-04-02
- **Detail**: True parallel execution in Claude Code requires all agent calls in ONE message block. Sequential deployment (one Agent call per message) serializes the pipeline and loses all parallelism benefit. Pattern: one message with Agent_A + Agent_B + Agent_C calls simultaneously. Exception: only serialize when Agent B's prompt depends on Agent A's specific output. Design agent prompts to be independent where possible.

### [SL-034] VERIFIED Data Floor: ≥2 independent T1-T3 sources required before implementation clears gate
- **Source skill**: holy-trinity v3.0, profTeam v3.0
- **Confirmed by**: User directive (2026-04-02) — "ONLY use cross verified information with VERIFIABLE sources"
- **Applies to**: holy-trinity, profTeam, ALL skills proposing implementations based on research
- **Confidence**: HIGH (user directive — non-negotiable)
- **Last validated**: 2026-04-02
- **Detail**: Source tier system: T1=Official docs/API reference, T2=GDC/AAA postmortems/named practitioners, T3=Peer-reviewed academic, T4=Engine source analysis, T5=Community tutorials. VERIFIED classification requires ≥2 independent T1-T3 sources. Single T1-T3 = PROBABLE. T4/T5 only = UNVERIFIED — tagged and blocked from implementation pipeline. **Engine-Version Exception**: For engine-version-specific topics where T1 docs don't exist — T4 (engine source) + T2 (GDC/practitioner) = VERIFIED, tagged `[VERIFIED-ENGINE-SOURCE]`. Engine source is ground truth when docs lag (per SL-030). Enforced at Holy Trinity Phase 2.5 Verifiable Data Gate.

### [SL-035] Additive-only discipline: skill/tool upgrades layer ON TOP — zero removals without user approval
- **Source skill**: holy-trinity v3.0
- **Confirmed by**: User directive (2026-04-02) — "ensure we dont get rid of valuable information"
- **Applies to**: holy-trinity, ALL skills that modify other skill files or .claude/ infrastructure
- **Confidence**: HIGH (user directive — non-negotiable)
- **Last validated**: 2026-04-02
- **Detail**: When Holy Trinity or any skill modifies SKILL.md files, _learnings.md, shared infra, or any .claude/ file: ZERO REMOVALS without explicit user approval. Every upgrade is an additive layer — new sections, steps, rules added ON TOP of existing content. Existing content preserved verbatim unless factually incorrect. Restructuring or removal flagged as [FLAG: REMOVAL NEEDED] and blocked pending user decision. Skill files contain accumulated knowledge — removal of any section erases validated learnings.

<!-- SL-038 to SL-042: Moved to _shared_learnings_ue5.md (UE5 domain) -->

## Self-Improvement Infrastructure (2026-04-02)

### [SL-043] Shared learnings IDs must be globally unique — check max ID before appending
- **Source skill**: init (Holy Tools audit, 2026-04-02)
- **Confirmed by**: 3 duplicate SL-ID pairs found during audit (SL-033/034/035 each used twice)
- **Applies to**: ALL skills appending to _shared_learnings.md
- **Confidence**: HIGH (data integrity issue verified — caused ambiguous cross-references)
- **Last validated**: 2026-04-02
- **Detail**: Before appending a new SL entry, grep for the highest existing SL-NNN ID and use SL-(N+1). Two concurrent sessions appended SL-033/034/035 independently, creating duplicate IDs with completely different content. This broke all cross-referencing. Fixed by renumbering duplicates to SL-038/039/040 and SL-036/037 to SL-041/042. Next available: SL-044. **Protocol**: Always `grep "SL-" _shared_learnings.md | sort -t- -k2 -n | tail -1` before assigning a new ID.

### [SL-044] Learning pipeline health: count entries per skill to detect silent failures
- **Source skill**: init (Holy Tools audit, 2026-04-02)
- **Confirmed by**: devTeam has 2 entries vs 125 for holy-trinity despite many invocations
- **Applies to**: ALL skills with Post-Invocation Learning Protocol
- **Confidence**: HIGH (learning imbalance indicates protocol not firing consistently)
- **Last validated**: 2026-04-02
- **Detail**: During init upgrade checks, count `_learnings.md` entries per skill. If a skill has <5 entries after 10+ known invocations, flag as "learning pipeline broken" — the Post-Invocation Learning Protocol is silently failing. Root cause is usually context compaction eating the learning step at end of long sessions. Mitigation: write learnings INCREMENTALLY during execution (after each significant discovery), not just at the end. Entry counts as of 2026-04-02: devTeam=2, profTeam=58, holy-trinity=125, cycle=70, professor=11, blueprint=2, init=4.

### [SL-045] Dependency graph and shared infra must be version-synced with skill SKILL.md versions (CONFIRMED 2026-04-08)
- **Source skill**: init (Holy Tools audit, 2026-04-02)
- **Confirmed by**: Dependency graph showed v2.0 while all 3 Holy Tools were at v3.0
- **Applies to**: ALL skills that reference version numbers in shared infrastructure
- **Confidence**: HIGH (version mismatch creates confusion about which protocols are active)
- **Last validated**: 2026-04-02
- **Detail**: When a skill's SKILL.md is upgraded to a new version (e.g., v2.0→v3.0), the dependency graph (`skill_dependency_graph.md`) and any shared infrastructure that references that version must be updated in the same session. The version in the dependency graph is the "truth" that other skills read to understand capabilities. Stale versions cause skills to use outdated protocols.

## v4.0 Self-Learning Infrastructure (2026-04-08)

### [SL-046] Incremental learning writes fix broken pipelines — write at milestones, not end-of-session
<!-- meta: { "run_id": "upgrade_v4_20260408", "domain": "skills", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-08" } -->
- **Source skill**: devTeam v4.0 upgrade (2026-04-08)
- **Confirmed by**: SL-044 root cause analysis (devTeam had 2 entries vs 125+ invocations)
- **Applies to**: ALL skills with Post-Invocation Learning Protocol
- **Confidence**: HIGH (root cause confirmed: context compaction eats end-of-session writes)
- **Last validated**: 2026-04-08
- **Detail**: Learning entries MUST be written DURING execution at specific milestones (after scoring, after anti-patterns, after regression check), not queued for end-of-session. Context compaction in long sessions (6-15 hrs typical) kills batched writes. Even a single scoring checkpoint surviving compaction is infinitely more valuable than zero entries. Protocol defined in devTeam v4.0 Incremental Learning Checkpoint Protocol and shared protocols v2.0 §5.

### [SL-047] Calibration echo feedback loop enables self-improving diagnostic accuracy
<!-- meta: { "run_id": "upgrade_v4_20260408", "domain": "skills", "confidence": "MEDIUM", "confirmed_count": 0, "roi_score": 4, "staleness_check": "2026-04-08" } -->
- **Source skill**: devTeam v4.0 upgrade (2026-04-08)
- **Confirmed by**: N/A (new v4.0 mechanism — needs validation across 3+ runs)
- **Applies to**: devTeam, holy-trinity
- **Confidence**: MEDIUM (theoretical — derived from calibration weight drift observed in 125+ runs but never measured)
- **Last validated**: 2026-04-08
- **Detail**: After every devTeam review, compare predicted top-3 gap dimensions (from calibrated weights) to actual top-3 gaps found. Track prediction_accuracy = overlap / 3. Weights that consistently miss get downweighted; weights that consistently hit get upweighted. This creates a closed feedback loop: more reviews → better weights → more accurate diagnoses. Requires the incremental learning fix (SL-046) to be active so calibration data accumulates.

### [SL-048] Query ROI tracking makes research agents smarter over time
<!-- meta: { "run_id": "upgrade_v4_20260408", "domain": "skills", "confidence": "MEDIUM", "confirmed_count": 0, "roi_score": 4, "staleness_check": "2026-04-08" } -->
- **Source skill**: profTeam v4.0 upgrade (2026-04-08)
- **Confirmed by**: N/A (new v4.0 mechanism — needs validation across 3+ runs)
- **Applies to**: profTeam, professor
- **Confidence**: MEDIUM (logical extension of existing agent ROI tracking which is proven HIGH confidence)
- **Last validated**: 2026-04-08
- **Detail**: Track individual search query ROI (HIGH/MEDIUM/LOW) per agent per topic type. Before deploying future agents, inject HIGH-ROI query patterns as "PROVEN QUERIES" and flag LOW-ROI patterns as "AVOID". Over time, agents develop topic-type-specific query expertise — architecture queries learn which GDC phrasings work, debugging queries learn which error-pattern phrasings find root causes. Extension of existing Agent ROI Leaderboard (which tracks per-agent ROI) to per-query granularity.

## Cross-Skill Promotions (2026-04-09 Ecosystem Audit)

### [SL-049] UE5 Python CANNOT modify AnimGraph topology — C++ required
<!-- meta: { "run_id": "your-automation-skill_v05_20260409", "domain": "UE5", "confidence": "HIGH", "confirmed_count": 3, "roi_score": 5, "staleness_check": "2026-04-09" } -->
- **Source skill**: your-automation-skill (2026-03-28), updated 2026-04-09
- **Confirmed by**: your-automation-skill (empirical), community docs (verified), UE5 source code audit (2026-04-09)
- **Applies to**: ALL skills planning UE5 AnimBP automation
- **Confidence**: HIGH (multiple attempts failed via Python, C++ approach verified against UE5 5.7 source)
- **Last validated**: 2026-04-09
- **Detail**: UE5 Python Remote Execution CANNOT modify AnimGraph topology — `AnimGraphNode_*` classes are not exposed to Python. BUT native C++ CAN: `UEdGraph::AddNode()`, `UEdGraphPin::MakeLinkTo()`, `UEdGraphSchema::TryCreateConnection()` all work on AnimGraph nodes. Your-Automation-SkillBridge v0.5 implements 8 C++ AnimGraph tools that do this via HTTP JSON-RPC. Key API patterns: AddNode BEFORE PostPlacedNewNode (order matters), state rename via `FBlueprintEditorUtils::RenameGraphWithSuggestion()` on BoundGraph, FindObject class paths use no U/A/F prefix. Priority: C++ Your-Automation-SkillBridge > Python Remote Exec > Vision automation.

### [SL-050] FP32 training mandatory on Pascal GPUs (GTX 1070) — bf16/fp16 causes silent failures
<!-- meta: { "run_id": "ecosystem_audit_20260409", "domain": "ML", "confidence": "HIGH", "confirmed_count": 3, "roi_score": 5, "staleness_check": "2026-04-09" } -->
- **Source skill**: project-init (2026-03-26, Sessions #2 and #4)
- **Confirmed by**: project-init Session #2 (CUDA install), Session #4 (bitsandbytes NF4 bf16 leak), enigma-init (implicit — all ML on same hardware)
- **Applies to**: ALL skills involving ML training on user's hardware
- **Confidence**: HIGH (3 independent failures confirmed the constraint)
- **Last validated**: 2026-04-09
- **Detail**: On GTX 1070 (Pascal architecture), bitsandbytes NF4 dequantization leaks bf16 tensors during backward pass, causing `_amp_foreach_non_finite_check_and_unscale_cuda not implemented for BFloat16`. Fix: set `bnb_4bit_compute_dtype=torch.float32`, `fp16=False`, `bf16=False`, `optim="adamw_torch"`. Also: DPO on stacked LoRA adapter + 4-bit quantization + gradient_checkpointing causes tensor shape mismatch on Pascal — merge SFT adapter into base weights first. User hardware: GTX 1070 8GB, i5-9600K, 16GB RAM.

### [SL-051] bitsandbytes NF4 backward pass leaks bf16 tensors on Pascal — use float32 compute dtype
<!-- meta: { "run_id": "ecosystem_audit_20260409", "domain": "ML", "confidence": "HIGH", "confirmed_count": 2, "roi_score": 4, "staleness_check": "2026-04-09" } -->
- **Source skill**: project-init Session #4 (2026-03-26)
- **Confirmed by**: project-init (empirical, 2 separate training attempts)
- **Applies to**: ALL skills deploying quantized models for training
- **Confidence**: HIGH (reproducible failure with clear fix)
- **Last validated**: 2026-04-09
- **Detail**: Specific to bitsandbytes 4-bit NF4 quantization on Pascal GPUs: gradient checkpoint recomputation produces different shapes/dtypes than saved tensors when using bf16 compute. The fix is `bnb_4bit_compute_dtype=torch.float32`. This is separate from the general fp16/bf16 incompatibility — it's a specific interaction between NF4 dequantization and gradient checkpointing. Affects any LoRA + QLoRA training pipeline on Pascal.

### [SL-052] UE5 UBT does NOT discover new .cpp files without project regeneration
<!-- meta: { "run_id": "your-automation-skill_deploy_20260409", "domain": "UE5", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "staleness_check": "2026-04-09" } -->
- **Source skill**: godspeed (2026-04-09 Your-Automation-Skill deploy)
- **Confirmed by**: empirical — plugin loaded with 10/22 tools after adding 14 new files
- **Applies to**: ALL skills deploying new C++ files to UE5 plugins
- **Confidence**: HIGH (observed: Your-Automation-SkillBridge loaded old tools only, new .cpp invisible to compiler)
- **Last validated**: 2026-04-09
- **Detail**: UnrealBuildTool (UBT) caches the source file list. Adding new .cpp/.h files to a plugin directory does NOT make them compile on next editor launch or Live Coding. You MUST: 1) Close UE5 editor, 2) Right-click .uproject → "Generate Visual Studio project files", 3) Rebuild. Only then does UBT re-scan directories and discover new source files. Modifying EXISTING files works with Live Coding, but NEW files are invisible until regeneration.

### [SL-053] Old design doc gap lists drift from reality — re-audit source before planning
<!-- meta: { "run_id": "godspeed_weapon_anim_ui_20260409", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-09" } -->
- **Source skill**: godspeed (2026-04-09 weapon animation research)
- **Confirmed by**: Combat Master Blueprint gap audit — 3 of 9 listed "gaps" were already closed in code 4+ days later
- **Applies to**: blueprint, profTeam, holy-trinity, devTeam, godspeed, ALL skills that reference older design docs
- **Confidence**: HIGH (verified against SWAnimInstance.cpp line numbers)
- **Last validated**: 2026-04-09
- **Detail**: Design documents describe a point-in-time gap analysis. In an active codebase (6-15 hour sessions, high velocity), gaps close quickly without the design doc being updated. Before writing implementation plans based on an older design doc, grep the source code for each listed gap. The bigger the time delta between doc creation and current session, the higher the chance gaps are closed. Planning work against a stale gap list wastes planning time AND produces misleading "phase order" recommendations. Always audit: read the relevant .cpp file, grep for the feature name, verify what's actually wired. Only then accept the doc's gap list or update it.

### [SL-054] UBT "Target is up to date" false negative — touch files to force rebuild
<!-- meta: { "run_id": "godspeed_ubt_touch_20260409", "domain": "UE5", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 3, "staleness_check": "2026-04-09" } -->
- **Source skill**: godspeed (2026-04-09 UI rebuild)
- **Confirmed by**: Empirical — first build 1.69s "up to date", touch + second build 73.25s compiled 5 files
- **Applies to**: verify, godspeed, ALL skills that trigger UE5 C++ rebuilds
- **Confidence**: HIGH (reproducible, clear fix)
- **Last validated**: 2026-04-09
- **Detail**: When Build.bat reports "Target is up to date" after source edits, UBT's timestamp check is skipping because the output binary (.dll) mtime is newer than the source files. This happens when Live Coding or a previous build ran AFTER the edits were saved but BEFORE the manual Build.bat call. Fix: `touch` the edited .cpp files to update their mtimes, then rebuild. Single bash line: `touch file1.cpp file2.cpp && Build.bat ...`. Distinct from SL-052 (which is about NEW .cpp/.h files not being discovered — that needs project regeneration). Alternative: pass `-Clean` flag to Build.bat for a full clean rebuild (slower, ~4-5 min instead of 73s incremental).

### [SL-055] Prior-phase audit files are a goldmine of anti-patterns for extending-phase blueprints
<!-- meta: { "run_id": "cycle_enigma_vault_20260409", "domain": "skills", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-09" } -->
- **Source skill**: cycle (2026-04-09 your-study-project Phase 9 Vault Blueprint)
- **Confirmed by**: Phase 9 blueprint explicitly avoided all 48 anti-patterns documented in research/audit_phases6_8.md (P6-17 XSS, P6-09 regex false positives, P8-01 hardcoded drift, X-01 no mypy, X-02 custom runners, X-04 sys.path hacks)
- **Applies to**: blueprint, cycle, profTeam, holy-trinity, godspeed, feature-dev — ALL skills planning a new phase/feature in a multi-phase project
- **Confidence**: HIGH (validated on first application — Phase 9 blueprint reused audit findings directly as "what NOT to do" list)
- **Last validated**: 2026-04-09
- **Detail**: When a multi-phase project (enigma, project-init, your-project, forge3d, quantified) has existing audit files (audit_phaseN_M.md, code_review_N.md, devTeam_review_N.md) from earlier phases, those audits are the fastest path to anti-pattern discovery for the NEXT phase. The audits already documented what went wrong before, usually with severity labels and concrete evidence. A blueprint for Phase N+1 should explicitly list the prior-phase anti-patterns it avoids — this reuses validated findings and demonstrates active learning from past mistakes. **Protocol**: Before writing a new-phase blueprint, grep `research/` or `Docs/Research/` for files matching `audit_*.md`, `*_review_*.md`, or `*_findings_*.md`. Read the CRITICAL and HIGH severity findings. Add an "Anti-patterns explicitly avoided" section to the new blueprint that references specific finding IDs (e.g., "P6-17: HTML XSS in report generator"). This pattern is orthogonal to SL-053 (which is about outdated GAP lists drifting from reality) — SL-055 is about reusing validated LEARNING from prior audits, not reusing stale gap analyses.

### [SL-056] IDE-vs-external-edit race clobbers Claude's edits when user has files open
<!-- meta: { "run_id": "godspeed_bpdoctor_api_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 BPDoctor API re-apply cycle)
- **Confirmed by**: empirical — added BPDOCTOR_API to 3 BPDoctor headers, rebuilt successfully. User reported "another bridge error" on editor relaunch. Investigation showed BPDoctor.dll had been rebuilt at a LATER timestamp without the exports. User's Visual Studio had the headers open; a save event overwrote the external edits with its stale in-memory buffer.
- **Applies to**: ALL skills that use the Edit tool on files the user may have open in an IDE (Visual Studio, Rider, VS Code, etc.) — especially during live coding sessions where the user is actively editing nearby files
- **Confidence**: HIGH (mechanically reproducible any time IDE is open and autosave/save fires after Claude's Edit)
- **Last validated**: 2026-04-10
- **Detail**: When Claude uses the Edit tool on a file that's currently open in the user's IDE, the IDE holds a pre-edit version in memory. If the user presses Ctrl+S, or autosave fires, or the IDE's "reload externally changed files" dialog is dismissed with "Keep Local", the IDE overwrites Claude's external changes with its own stale buffer. The rebuild then runs against the clobbered file and silently produces a binary that's missing the edit. **Prevention**: (1) Before editing files likely to be open in the IDE — headers being actively worked on, files the user just mentioned editing, files near recent user-written code — tell the user explicitly "close X, Y, Z in your IDE, or if it shows 'file changed externally' click RELOAD not Keep Local". (2) After the Edit tool returns, grep the file to confirm the change is present before triggering the build. (3) If the rebuild completes but behavior suggests the edit didn't apply (e.g., same symbol errors as before the fix), re-grep the file — IDE clobber is a common cause, not a rare one. **Detection signal**: file mtime is newer than Claude's last edit, AND the edited content is missing, AND the user was working on related files. **Recovery**: re-apply the edit, then immediately rebuild before the IDE can save again. **Distinct from UBT false-positive "target is up to date"** — that one means the source IS correct but UBT skipped the rebuild; IDE clobber means the source itself is WRONG. Also see `_shared_learnings_ue5.md` SL-061 for the incident-specific write-up.

### [SL-062] Shared protocols v2.1: cache discipline + filtered loads + consolidated recovery primitives close critical efficiency gaps
<!-- meta: { "run_id": "ecosystem_efficiency_audit_20260410", "domain": "skills", "confidence": "HIGH", "confirmed_count": 3, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 holy-trinity max trinity + profTeam + devTeam ecosystem audit)
- **Confirmed by**: 3 independent audit agents converged on identical top findings — profTeam research agent (T1 Anthropic + T3 arxiv sources), devTeam architecture scoring (7 Laws → 23/35 Grade C), Explore concrete-scan (file:line references across 29+ skills)
- **Applies to**: ALL skills (holy-trinity, devTeam, profTeam, godspeed, cycle, professor, blueprint, debug, all 6 project inits, all Tier 2-3 tools)
- **Confidence**: HIGH (3-agent cross-validation, scored against 7 Laws, T1/T3 source backing)
- **Last validated**: 2026-04-10
- **Detail**: Ecosystem audit identified Law 5 (Code is Liability) at 2/5 as the worst dimension — driven by monolithic SKILL.md files (holy-trinity 739 LOC, devTeam 594 LOC, profTeam 494 LOC) and duplicated content across 5+ skill files (failure recovery catalogs, escalation ladders, regression guard protocols, session state persistence patterns). Shared protocols upgraded to v2.1 with 4 new sections + §1 enhancement, all additive per SL-035. **§1 enhancement**: grep-first filtering mandatory before reading `_shared_learnings.md` — loads ~40 matching lines instead of the full 336 (saves ~8-12K tokens per invocation). **§12 Prompt Cache Discipline**: order agent prompts invariant → semi-stable → volatile for 10× cache discount (50-80% cost reduction expected on repeated-prefix workloads per Anthropic Prompt Caching docs). **§13 Failure Recovery Primitives**: single canonical table consolidates recovery catalogs. **§14 Session State Persistence**: canonical directory pattern + manifest.json schema for all checkpointing skills. **§15 Query ROI Tracking Schema**: closes the SL-048 feedback loop with concrete per-query tagging + aggregation + proven-query injection (30-40% search cost reduction after 10+ runs per topic-type). Audit baseline: 23/35 Grade C. Target post-upgrade: ~29/35 Grade B. **Remaining gaps (pending user greenlight)**: (a) monolithic SKILL.md progressive disclosure split (holy-trinity 739 → ~420 LOC), (b) Sonnet-default for profTeam research subagents (5× cost reduction at ~1% quality delta), (c) your-automation-skill shared-infra integration (zero protocol reference currently — silent learning pipeline on highest-volume Tier 2 tool), (d) SL-046 incremental checkpoint propagation to 15+ non-Holy-Tool skills (blueprint, cycle, professor, your-qa-skill, marketbot, finder, scanner, organizer, all 6 project inits), (e) SL-047 Calibration Echo propagation to profTeam/trinity/godspeed (self-improving accuracy loops), (f) staleness sweep enforcement at init skill (SL-001–SL-018 approaching 60-day threshold silently), (g) **SL-056 collision** between `_shared_learnings.md` (IDE-vs-external-edit) and `_shared_learnings_ue5.md` (bForceRootLock) — same ID different content, violates SL-043 globally-unique mandate; UE5 SL-061 also duplicates universal SL-056 content.

### [SL-063] State-flag lifetime audit: invert the condition when flag lifetime < effect duration
<!-- meta: { "run_id": "godspeed_movement_teleport_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 movement session)
- **Confirmed by**: User-confirmed fix ("wow dodge roll feels great") after two failed attempts using alpha fade + state flag checks
- **Applies to**: ALL skills writing code that gates visual/behavioral effects on state flags
- **Confidence**: HIGH (resolved 3 different teleport symptoms with a single architectural change)
- **Last validated**: 2026-04-10
- **Detail**: When writing `if (condition A) apply_effect()`, the gate must match the EFFECT's lifetime, not a related but shorter-lived state flag. In your project, `bIsDodging` cleared at 0.35s (i-frame timer) while the Mixamo dodge montage played for 1.5s. Gating the pelvis shift on `bIsDodging` meant the shift dropped at 0.35s leaving the mesh at max baked pelvis offset → visible teleport. Attempted fix with a smoothed alpha fade was an ANTI-PATTERN (produced `(1-alpha)*offset` residual drift). Real fix: INVERT the condition to check the NARROWEST negative exclusion — "skip shift iff combat montage active" where combat flags are sync with combat anims. Pattern: (a) audit flag lifetimes vs effect durations, (b) if mismatch, either track the effect directly (montage pointer) OR invert to exclude only the smallest case whose flag lifetime DOES match. Inversion is usually cleaner than grace timers.

### [SL-064] Symptom-vs-root-cause drift: scan log for unrelated warnings before accepting user's bug framing
<!-- meta: { "run_id": "godspeed_movement_teleport_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 movement session)
- **Confirmed by**: User-reported "crouch is really messed up, can't uncrouch or move" → actual cause was `LakeCollisionComponent` penetration, nothing to do with crouch
- **Applies to**: ALL skills handling user bug reports, debug, holy-trinity, devTeam
- **Confidence**: HIGH (one event but pattern is generally applicable and the cause was buried 2 hops from the symptom)
- **Last validated**: 2026-04-10
- **Detail**: User bug reports describe SYMPTOMS filtered through the user's mental model. The actual root cause can be 2+ causal hops away in a completely different subsystem. In your project: user said "can't uncrouch", meaning is "crouch is broken". Real cause: character penetrated a UE5 Water plugin `LakeCollisionComponent` because `UpdateSwimState` only queried procedural water tiles and missed AWaterBody actors. Character stuck in blocker → capsule can't resize → crouch can't resize → "can't uncrouch". Before accepting the user's framing as the debug target, ALWAYS grep the log (or tell user to check) for unrelated warnings in the seconds/minutes before the symptom. Common false-symptom anchors: "stuck and failed to move" CMC events, physics penetration warnings, missing asset warnings, collision channel mismatches. Extends SL-053 (doc staleness): the user's mental model of what's broken is itself a form of stale context that needs verification against ground-truth logs.

### [SL-065] The Shell Pattern: file existence ≠ implementation — always verify depth before declaring "done"
<!-- meta: { "run_id": "godspeed_gap_audit_deep_drill_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 your project deep gap drill)
- **Confirmed by**: Deep-drill audit found 46 Item DataAssets at 1.5-2KB each (empty shells), SWCraftingSystem.cpp with 6 TODOs in core methods, SWFireComponent hardcoded `Dmg = 30.f`, Economy/Achievement subsystems falsely flagged as orphans by Pass-1 agent. Pass-1 file-count audit missed ALL of these.
- **Applies to**: ALL skills doing gap audits, sitrep, close-session, holy-trinity, godspeed, code reviews
- **Confidence**: HIGH (one audit but the pattern was consistent across 3+ independent systems in one codebase — generalizable)
- **Last validated**: 2026-04-10
- **Detail**: In any large solo-dev or rapid-iteration codebase, systems get scaffolded to completeness then data-populated to emptiness. File existence is NOT proof of implementation. Always drill into: (1) file size — a 1.8KB .uasset is almost certainly an empty class reference, same for 100-line .cpp with only method signatures; (2) TODO/FIXME grep — scan every .cpp for `TODO|FIXME|HACK` before declaring a system "done"; (3) method body inspection — signatures exist but bodies may be empty or pass-through; (4) reference counting — "grep found it in 25 files" may just mean it's declared 25 times, not invoked 25 times; (5) directory vs catalog — a folder with 46 .uasset files may contain 46 empty shells. Distinguish 4 states: **orphaned** (no references at all), **scaffolded** (class exists, methods are TODOs), **internally wired** (used by other subsystems but not gameplay), **fully wired** (used from gameplay execution paths). These look identical at first glance but have very different gap-closure costs. Rule for audit output: "46 files exist" must never be reported as "46 things are done" — always sample file sizes or grep TODOs and report the distinction.

### [SL-066] Cross-check TOMORROW_*.md / TODO_*.md against project_status.md before execution
<!-- meta: { "run_id": "godspeed_delivery_audit_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 your project delivery audit)
- **Confirmed by**: Pulled TOMORROW_TASK_LIST.md as critical path item #1 (Bug #29 montage slot fix). Cross-check of project_status.md revealed Bug #29 was RESOLVED 2026-03-28d via a completely different approach (Montage_Play + save-attack pattern). Task list was stale initial-diagnosis doc that nobody cleaned up. Would have wasted cycles executing ghost steps or regressing to stale code.
- **Applies to**: ALL skills acting on previously-written plan/task/roadmap docs — godspeed, holy-trinity, close-session, init, sitrep, any project init
- **Confidence**: HIGH (one incident, but the anti-pattern is generally applicable to any long-lived project with TODO/ROADMAP docs)
- **Last validated**: 2026-04-10
- **Detail**: Before treating any TOMORROW_*.md, ROADMAP_*.md, TODO_*.md, or "next steps" doc as authoritative, cross-check the latest N entries in `project_status.md` (or equivalent session-history file). A task doc older than the most recent session may describe a bug that has already been fixed via a different approach, OR describe "applied fixes" that no longer match the codebase. Protocol: (1) For any plan doc older than 48 hours, grep its listed bugs against the 3-5 most recent session entries in project_status.md. (2) If a "fix applied" line in the task doc references specific C++ code/line numbers, verify the code matches — if it diverges, the task doc is stale. (3) When stale state is found, generate a successor doc (e.g. `TOMORROW_GODSPEED_HANDOFF.md`) and explicitly mark the predecessor as superseded. (4) Never revert current working code to match a stale task doc's assumptions — the current code is the source of truth. Reinforces Sacred Rule #3 (Confirmed fixes are SACRED) — includes fixes documented in session history, not just in comments.

### [SL-067] Windows cp1252 — ASCII-only in print statements for any subprocess-captured Python
<!-- meta: { "run_id": "godspeed_toke_brain_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 2, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 your-3d-skill v5.3 sprint)
- **Confirmed by**: [1] your-3d-skill v5.3 (bridge modules with box-drawing chars). [2] godspeed Toke Brain build (2026-04-10 evening) — severity_classifier.py had `→` (U+2192) in its reasoning string, brain_tests.py crashed on `print(f"    reasoning: {result.reasoning}")` with `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'`. Same root cause, different skill context (Python meta-tooling vs Blender bridge). **Additional fix pattern discovered this session**: `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` at the top of the script as a belt-and-suspenders defensive measure — handles any Unicode that sneaks in via config files, error messages, skill names, etc. Works on Python 3.7+ via `io.TextIOWrapper.reconfigure()`. Wrap in `try/except (AttributeError, OSError)` for safety on non-standard streams.
- **Original confirmation**: Wrote 8 new bridge modules with Unicode box-drawing chars (U+2500 horizontal box, U+2192 right arrow, U+2014 em dash, U+2194 left-right arrow, U+0394 delta) in print statements for decorative dividers and tables. Smoke test `python bible_routing.py --type weapon --sub-type sword` crashed with `UnicodeEncodeError: 'charmap' codec can't encode character`. Existing v5.2 modules worked because their Unicode chars were only in comments/docstrings — source is read as UTF-8 regardless of locale, only stdout decoding fails.
- **Applies to**: ALL Python modules on Windows whose stdout is captured by `subprocess.run(..., text=True)` — your-3d-skill bridge, Your-Automation-Skill, your-trading-project host-side tools, any CLI invoked by another Python process
- **Confidence**: HIGH (one incident, but mechanism is deterministic — Windows default cp1252 encoding lacks mappings for these codepoints)
- **Last validated**: 2026-04-10
- **Detail**: On Windows, `subprocess.run(text=True)` decodes captured stdout using `locale.getpreferredencoding()` which defaults to cp1252. cp1252 has no mapping for common decorative Unicode chars. A single such char in a print statement crashes the PARENT process when it tries to decode the child's output. **Four-part fix:** (1) Write new modules with ASCII-only in print statements — use `-` not box-drawing, `->` not right arrow, `-` not em dash, `<->` not left-right arrow, `Delta` not Greek delta. Unicode in comments/docstrings is fine because Python 3 reads source as UTF-8 regardless of Windows locale. (2) Add defensive decoding to any subprocess.run call that captures stdout from a child that might emit Unicode: `subprocess.run(..., text=True, encoding='utf-8', errors='replace')` — this both handles Blender's UTF-8 output correctly and degrades gracefully (`?` substitution) if an unexpected codepoint appears. (3) Verification step before ship: enumerate non-ASCII codepoints in print-context lines of each new module — `for line in open(fn): if 'print(' in line: bad = [c for c in line if ord(c) > 127]`. (4) **NEW from Toke Brain (2026-04-10)**: add `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` and same for stderr at the top of any Python script that might emit Unicode. This is a defensive belt-and-suspenders that catches anything the ASCII-discipline approach misses (e.g., strings loaded from TOML/YAML/JSON config files with em-dashes, skill names with Unicode, third-party error messages). Wrap in `try/except (AttributeError, OSError)` for safety. Rule of thumb: **treat ASCII as the stdout contract for any Python on Windows, AND add the reconfigure call as a safety net.** Applies in reverse too: on macOS/Linux, locale is usually UTF-8 so the issue doesn't surface — bugs lie dormant until someone runs on Windows.

### [SL-068] Claude Code hooks CANNOT force-switch the main session's model for the next turn
<!-- meta: { "run_id": "godspeed_toke_brain_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 Toke Brain model router build)
- **Confirmed by**: Agent A deep-dive research into `code.claude.com/docs/en/` during Toke Brain synthesis. The docs explicitly confirm: SessionStart hook can READ the current model but no hook output field exists to force-switch the main session's model for subsequent Claude turns. A `type: prompt` hook can declare its own `model:` for evaluating the hook's own prompt, but this governs hook evaluation only, not main session. MCP servers also cannot switch models (no protocol field for this).
- **Applies to**: ALL skills/hooks that might attempt hook-level model switching — model routers, cost optimizers, per-task automation, the Toke Brain itself
- **Confidence**: HIGH (sourced from official Claude Code docs, confirmed across multiple doc sections)
- **Last validated**: 2026-04-10
- **Detail**: The complete model-resolution priority stack in Claude Code (highest → lowest): `CLAUDE_CODE_SUBAGENT_MODEL` env var (subagents only) > `--model` CLI flag / `/model` slash command > `ANTHROPIC_MODEL` env var > `settings.json` model field > Agent tool per-invocation `model` param > subagent/skill frontmatter `model:` > plan default. Hooks have **zero write access** to this stack. **Implication for any router design**: must operate in two zones. Zone 1 = main session (advisory only — log, warn, suggest `/model`). Zone 2 = subagents + skills (automatic via env var + frontmatter + Agent tool model param). Do not attempt to build a hook that flips the main session model for the next turn — it will silently fail. The native closest analogs are: `opusplan` alias (auto Opus→Sonnet on plan/execute handoff) and `CLAUDE_CODE_SUBAGENT_MODEL` (blunt global override for all subagents). Integration-time mental model: "the main session is user territory, subagents/skills are the Brain's."

### [SL-069] LLM model router: scalar score prediction collapses — use hard gates + thresholds instead
<!-- meta: { "run_id": "godspeed_toke_brain_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 Toke Brain research)
- **Confirmed by**: Agent C literature review during Toke Brain synthesis. Multiple 2024-2026 papers document "routing collapse" as the #1 failure mode for LLM routers.
- **Applies to**: Any future work on LLM task routing, model selection, cost optimization — Toke Brain, and any downstream router built on top of it
- **Confidence**: HIGH (multiple independent sources in 2024-2026 literature)
- **Last validated**: 2026-04-10
- **Detail**: arxiv:2602.03478 ("When Routing Collapses") documents that score-prediction routers (MLPRouter, GraphRouter, EmbedLLM) trained to minimize prediction error degenerate at higher budgets — they route ~100% to the big model even when the small model is sufficient. Root cause: 94.9% of RouterBench queries have model-performance margins ≤ 0.05, so small prediction errors flip rankings catastrophically. The Oracle baseline only uses the strongest model for <20% of queries, so a well-calibrated router SHOULD route down aggressively. **Fix patterns that work**: (1) Pairwise ranking loss (EquiRouter approach) instead of scalar regression. (2) Hard gates + heuristic thresholds (LiteLLM complexity_router approach). (3) RouteLLM's sw_ranking with preference-weighted Elo. **Fix patterns that fail**: FrugalGPT-style post-generation cascading adds latency that exceeds savings in interactive contexts (like Claude Code). Embedding similarity alone captures topic but not difficulty. Static thresholds set on one benchmark don't transfer cross-domain. **Toke Brain applies this**: uses 7 weighted heuristic signals + 6 hard guardrails (GPQA-class, multi-file, long-context, creative, debug, architecture) instead of learned scalar score prediction. Literature is unanimous that hybrid (heuristics + hard gates) beats either alone in production, especially before outcome-data feedback loops exist.

### [SL-070] Claude Code `opusplan` alias: free automatic Opus→Sonnet handoff between plan and execute modes
<!-- meta: { "run_id": "godspeed_toke_brain_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 Toke Brain Agent A research)
- **Confirmed by**: `code.claude.com/docs/en/model-config` — the `opusplan` alias is listed alongside `opus`, `sonnet`, `haiku`, `best`, `default`, etc.
- **Applies to**: ALL sessions — the user's sessions, any cost-conscious workflow, any session that uses plan mode
- **Confidence**: HIGH (official Claude Code docs)
- **Last validated**: 2026-04-10
- **Detail**: `opusplan` is an alias that automatically switches between Opus (during plan mode) and Sonnet (during execution mode). Set via `claude --model opusplan` or `/model opusplan`. The model switch is handled natively by Claude Code — no orchestration code needed. **Why it matters**: plan mode is where reasoning happens (architect the fix, design the approach) and Opus's quality edge is material. Execution mode is where the diff gets applied (mechanical, structured) and Sonnet is within 1-2 pts of Opus. The `opusplan` alias captures exactly the right split for ~free. **Why it's unused**: it's buried in the docs as one alias among several, and the `/model` picker doesn't call it out as a recommendation. **Integration pattern**: either set `ANTHROPIC_MODEL=opusplan` in shell, or boot with `--model opusplan`, or run `/model opusplan` at session start. Most impactful for plan-heavy sessions (overnight unattended, architecture work, blueprint generation). Less impactful for pure-execution sessions (already Sonnet-appropriate).

### [SL-071] Anthropic `advisor_20260301` API tool: the INVERSION pattern that supersedes classical routing
<!-- meta: { "run_id": "godspeed_toke_brain_v2_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 Toke Brain v2 research burst, Agent 1)
- **Confirmed by**: Official Anthropic docs at https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool and launch blog at https://claude.com/blog/the-advisor-strategy (dated 2026-04-09 — ONE DAY before this discovery)
- **Applies to**: ALL skills that involve model routing, cost optimization, or multi-model orchestration. Especially holy-trinity, profTeam, godspeed, brain, and any future router design.
- **Confidence**: HIGH (first-party Anthropic docs + launch blog)
- **Last validated**: 2026-04-10
- **Detail**: Anthropic shipped `advisor_20260301` on 2026-04-09 — a first-party server-side API tool that INVERTS classical routing. Beta header: `anthropic-beta: advisor-tool-2026-03-01`. Classical routing: big model decomposes → delegates to small worker models. Advisor pattern: **small executor (Sonnet/Haiku) DRIVES end-to-end, escalates to Opus via the `advisor` tool only when stuck**. All in ONE `/v1/messages` request — no client-side orchestration, no session management overhead. The executor emits `server_tool_use` with empty `input`; Anthropic runs Opus inference server-side with the full transcript; Opus returns `advisor_tool_result` with plaintext advice (thinking blocks stripped). **Benchmarks published:** SWE-bench Multilingual: Sonnet 4.6 + Opus advisor = 74.8% (+2.7pp over Sonnet solo, −11.9% cost vs Opus solo). BrowseComp: Haiku 4.5 + Opus advisor = 41.2% (+109% over Haiku solo, −85% cost vs Sonnet solo). Supported pairs: Haiku→Opus, Sonnet→Opus, Opus→Opus (self-review). `max_uses` default 3 caps cost per request. **The tool is NOT yet exposed via a Claude Code slash command** — community `/advisor` references are third-party / premature. When Claude Code adds native slash-command integration, any router built today should slot this in as the escalation mechanism. **Implication for Toke Brain**: the v1 static classifier is architecturally DIFFERENT from the advisor inversion. v2 added `[advisor]` section to the manifest documenting the v3 integration slot. When native Claude Code support lands, Brain will auto-recommend advisor mode for S3/S4 multi-step tasks. Do not design routing systems without considering this pattern as the upstream primitive.

### [SL-072] Extended thinking budget on Sonnet 4.5/4.6 BEATS Opus 4.6 on SWE-bench — drop-in quality amplification
<!-- meta: { "run_id": "godspeed_toke_brain_v2_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 Toke Brain v2 research burst, Agent 2)
- **Confirmed by**: Anthropic's Sonnet 4.5 launch numbers + extended thinking docs at https://platform.claude.com/docs/en/build-with-claude/extended-thinking
- **Applies to**: ALL skills that invoke Sonnet/Opus for reasoning-heavy work — devTeam, profTeam, blueprint, holy-trinity, brain, debug, analyst
- **Confidence**: HIGH (Anthropic published numbers)
- **Last validated**: 2026-04-10
- **Detail**: Sonnet 4.5 with a 200K-token extended thinking budget scores **82.0% on SWE-bench Verified vs Opus 4.6's 80.8%** — Sonnet with thinking literally BEATS Opus without. 32K budget costs ~$0.096 extra per call. API parameter: `thinking: {type: "enabled", budget_tokens: 32000}`. Implementation difficulty: **1/5 (drop-in)**. **This is the single highest-ROI quality amplification technique available today.** For any task where Sonnet is almost-good-enough but you were tempted to escalate to Opus, try Sonnet-with-thinking first — often closes the gap for under $0.10 extra. Brain v2 encodes this as `extended_thinking_budget` in the tier_map: S3=16K, S4=32K, S5=64K. **Failure mode**: do NOT apply thinking to trivial tasks (S0/S1) — pure cost with no quality gain.

### [SL-073] Quality eval at personal scale: 30-prompt LLM-as-judge harness, $1/month, sensitive to 7-8% quality drop
<!-- meta: { "run_id": "godspeed_toke_brain_v2_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 Toke Brain v2 research burst, Agent 4)
- **Confirmed by**: Agent 4 synthesis of 2025-2026 LLM-as-judge literature (MT-Bench, Chatbot Arena methodology) applied to personal-scale routers
- **Applies to**: Any skill that routes between models and needs quality verification — brain, devTeam, profTeam, holy-trinity, debug, analyst
- **Confidence**: HIGH (Agent 4's synthesis is grounded in published methodology)
- **Last validated**: 2026-04-10
- **Detail**: For a personal router at ~200-300 sessions/month, the minimum viable quality eval is: **30 prompts × 3 categories (coding / reasoning / trivial), LLM-as-judge with Sonnet as the judge, rubric-based scoring (correctness 0-3, completeness 0-3, reasoning 0-2, code quality 0-2), position-swap averaged to eliminate order bias**. Cost per run: ~$0.23 at Sonnet pricing. Weekly cadence: ~$1/month. Sensitivity: ~7-8% quality delta detectable with N=30 (50 prompts for 5% delta at 80% power). Regression alerts via EWMA on tier distribution (1.5σ above 4-week baseline triggers warning). **Avoid**: shadow routing continuously (too expensive at $1K+/month), canary deploys (< 287 sessions/month is statistically underpowered), explicit thumbs-up UI (< 5% usage rate per GitHub internal metrics). **Use**: implicit signals — correction keyword detection, model override events, acceptance depth. Brain v2 has the harness STUB (eval/eval_prompts.json with 30 prompts + rubric); execution pipeline is v3 work.

### [SL-074] EWMA weight updater is the right feedback loop for scarce-signal personal routers — NOT bandits
<!-- meta: { "run_id": "godspeed_toke_brain_v2_20260410", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "staleness_check": "2026-04-10" } -->
- **Source skill**: godspeed (2026-04-10 Toke Brain v2 research burst, Agent 5)
- **Confirmed by**: Agent 5 synthesis of contextual bandit literature (LinUCB, Thompson Sampling, Vowpal Wabbit) applied to scarce-signal personal tools
- **Applies to**: Any skill that needs online learning from scarce user signals — brain, devTeam calibration echoes, profTeam ROI tracking
- **Confidence**: HIGH (bandit literature + scarcity analysis)
- **Last validated**: 2026-04-10
- **Detail**: **LinUCB / contextual bandits / neural bandits are WRONG for personal-scale tools with ~200-300 decisions/month.** Exploration penalty (deliberately making bad decisions to gather data) is unacceptable when quality matters. Matrix methods are unstable in the underdetermined regime (6 tiers × 8 signals × scarce labels). Convergence takes months. **Right pattern**: Exponentially Weighted Moving Average (EWMA) weight updater with small alpha (0.005), fed by implicit signals from existing telemetry. Signals: (1) model override event (recommended_model != model_used_in_next_tool_call), (2) correction follow-up (next prompt contains "fix this", "that's wrong", etc.), (3) session abandonment. Plus optional explicit `brain good`/`brain bad` commands (10× weight). **Thompson Sampling for signal diagnostics only** — Beta(alpha, beta) per signal reports per-signal accuracy in brain scan; tells operator which signals are trustworthy vs noise. **Drift alert**: 7-day vs 30-day tier distribution comparison; if any tier drifts > 10pp, warn. Brain v2 implements all of this in `brain_learner.py` (449 lines, stdlib only). **Do not retrain routers with learned approaches until you have 1000+ preference pairs** — at the user's rate, that's 3-4 months minimum. EWMA starts learning immediately.

### SL-080: Research-before-3rd-iteration — parallel agents unblock correction loops
<!-- meta: { "id": "SL-080", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "applies_to": "godspeed,holy-trinity,cycle,debug", "staleness_check": "2026-04-11", "source_tier": "T4" } -->
- **Finding**: When user rejection loops appear on the same fix target ("X is wrong" → patch → "Y is also wrong" → patch), spawning 2-3 parallel research agents on the DOMAIN (not the specific failure) extracts canonical techniques faster than a 3rd patch attempt. Codebase-map agent (Explore) is the highest-ROI of the 3 — it returns the exact constraint system the fix must honor.
- **Evidence**: 2026-04-11 SWInventoryWidget chrome — 2 rejections (BR2049 filigree + substance v1) → 3 parallel agents (Destiny/Cyberpunk/Control research 55s, Tarkov/Diablo/Division research 64s, SWInventoryWidget Explore bounds map) → v3 accepted on first build. Research ~2 min wall time. Previous 2 iterations ~15 min each of failed main-context Edit churn.
- **Protocol**: On 2nd user rejection of the same fix target on the same codebase region, STOP patching. Deploy 3 parallel agents: (1) domain-research-western, (2) domain-research-eastern, (3) Explore codebase map of the target file. Use their findings to rebuild v3 instead of attempting patch #3.
- **Why it works**: Patches fight symptoms; research finds the constraint system. The Explore agent's file map is load-bearing — it returns the real constants the fix must align to.
- **Cost cap**: 3 parallel agents, ~2 min wall time, 1 Opus main-context synthesis. Cheaper than a 15-min failed 3rd iteration.
- **Applies to**: godspeed (Phase 4 escalation ladder — insert between L2 instrument and L3 research), holy-trinity (before cycle 3), cycle (before final pass), debug (Phase 3 research fallback)
- **Related**: SL-056 (IDE clobber), SL-062 (v2.1 cache discipline), SL-079 (shell-append phase 0)

### SL-081: Dual-schema JSON extension for incremental migration
<!-- meta: { "id": "SL-081", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "applies_to": "author,toolsets,any JSON-backed router", "staleness_check": "2026-04-11", "source_tier": "T4" } -->
- **Finding**: JSON config files (toolsets.json, routing tables, manifests) can be extended per-entry with new fields without breaking consumers or validators, AS LONG AS consumers feature-detect missing fields: `entry.get("new_field") or entry["legacy_field"]`. Unlocks incremental enrichment without big-bang migration.
- **Evidence**: 2026-04-11 Author toolsets.json v1.4 — UI:1..UI:10 + UI:A enriched with `action`/`grep`/`resources`/`invoke_when` fields. Other zones (B:/U:/M:/G:/R:) remain thin v1. Validator still 64/64 PASS (validator reads only `primary`/`support`, ignores new fields). Live Python demo proved field access: `d['per_zone']['UI:2']['action']` returns the enriched imperative.
- **Protocol**: When extending a schema: (1) add new fields to PRIORITY entries only, (2) keep all legacy fields intact, (3) add a `schema_notes` block documenting both shapes, (4) consumers use `.get(field)` with legacy fallback, (5) run validator after to confirm backward compatibility.
- **Why it works**: No coordination needed with other entries or consumers. Each migration is self-contained. Rollback is trivial (delete new fields, legacy still works).
- **Applies to**: Any JSON-backed routing/config system in the ecosystem (Author toolsets, brain manifest, skill frontmatter, problem_class_routing.json)
- **Related**: SL-035 (additive-only discipline), SL-045 (version sync)

### SL-079: Shell-Append Phase 0 Protocol — 
<!-- meta: { "id": "SL-079", "confidence": "HIGH", "confirmed_count": 5, "roi_score": 5, "applies_to": "ALL", "staleness_check": "", "source_tier": "T4" } -->

**Finding**: Broken learning pipelines (devTeam, blueprint, your-automation-skill, marketbot, brain) were all caused by the same root: Edit-tool checkpoint writes inside phases get eaten by context compaction. Shell-append Bash writes at Phase 0 (BEFORE any Edit call) survive because they land on disk outside Claude context.

**Evidence**: 2026-04-10 toolset audit. 5 skills had v4.0 incremental checkpoint protocols documented but `_learnings.md` files stuck at baseline (devTeam 3 entries despite 125+ invocations, blueprint 22 lines, your-automation-skill 19 lines, marketbot 39 lines, brain 0 — no file). Applied shell-append Phase 0 fix. All 5 grew by +1 entry within the same audit run via shell-append dogfood verification. Fix is end-to-end operational.

**Confirmed by**: devTeam, blueprint, your-automation-skill, marketbot, brain (5 skills — auto-promotion threshold 2+ exceeded)

**Applies to**: ALL skills with _learnings.md pipelines

**Action**: For any skill whose pipeline is structurally broken despite documented "incremental checkpoint" protocols — check for Bash shell-append at Phase 0 before any Edit call. If absent, apply the pattern from `feedback_shell_append_protocol.md`. Verification wired into close-session Phase 4c (tri-state: marker+checkpoints → consolidate; marker only → partial warning; no marker → 🚨 regression flag) and init Step 0.5 (12-skill monotonic-growth expectation).

**Related**: SL-044 (pipeline silent failure), SL-046 (original "immediate checkpoint" protocol that did not fire), SL-062 (v2.1 ecosystem audit rationale). See memory `feedback_shell_append_protocol.md` + `project_toolset_audit.md`.

### SL-082: Feedback rules must be loaded BEFORE generating personalized output — 2026-04-11
<!-- meta: { "run_id": "shared_feedback_rule_precheck_20260411", "domain": "skills", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-04-11", "applies_to": ["analyst", "profTeam", "blueprint", "professor", "marketbot", "ALL personalized output skills"] }} -->
- **Finding**: Any skill producing personalized output for the user MUST load and check all `feedback_*.md` files from `~/.claude/projects/C--project-memory/memory/` BEFORE generating the output. Feedback files contain rules that directly constrain output shape (phrasing bans, framing requirements, truthfulness floors). Failing to load them leads to output that violates the user's explicit preferences.
- **Evidence**: 2026-04-11 analyst session generated `Jacob_Ribbe_Identity_Profile.pdf` Section 4 with peer-level comparisons to Tesla/Bohm/Coltrane/Fuller/Watts/McKenna. The rule `feedback_no_flattering_comparisons.md` — set earlier the same day in session 333de393 — explicitly forbids this pattern with the phrase `"'You're comparable to Wolfram / Bohm / Rovelli' = red flag phrasing. Avoid."` The PDF used this exact pattern across 6 figures. First-pass AND 5-agent verification pass both missed it. Caught only during close-session audit.
- **Applies to**: analyst, profTeam, blueprint, professor, marketbot, and ANY skill producing user-facing personalized output for the user.
- **Action**:
  1. Add "Feedback Rule Precheck" as a mandatory Phase 0 step to all personalized-output skills
  2. Enumerate every `feedback_*.md` file in `~/.claude/projects/C--project-memory/memory/` (use `ls` not `glob` — need full list)
  3. Read each feedback file — treat each as a hard constraint, not context
  4. Before delivering output, cross-check: does any section of the output violate any feedback rule?
  5. If yes: rewrite or omit before delivery. Do NOT ship the violation.
- **Cross-reference**: Relates to `feedback_truthful_answers.md` (SL parent) and `feedback_no_flattering_comparisons.md` (specific rule). This meta-learning says: **feedback rules are load-bearing, not optional.**

### SL-083: Structural Regex Outperforms Keyword Lists for Multi-Concern Detection — 2026-04-11
<!-- meta: { "run_id": "SL083_multi_concern_regex", "domain": "classifier/routing", "confidence": "HIGH", "confirmed_count": 2, "roi_score": 5, "staleness_check": "2026-10-11" } -->

**Finding**: Regex detecting STRUCTURE (3+ comma-separated items after —/:/with/that) catches multi-concern tasks that no keyword vocabulary can cover — because the verb/noun vocabulary is unbounded but the structural pattern is stable.
**Evidence**: brain audit 2026-04-11: `multi_concern_floor` regex fixed 5 wrong routings in one edit. Example: "implement X — verify A, update B, send C" correctly routed to S3 regardless of which verbs were used.
**Applies to**: brain, godspeed, ALL classifiers
**Action**: Before enumerating more keywords, ask: "Is there a structural pattern (commas, numbers, compound verbs) that characterizes this class?" Structural regex generalizes better. Keywords overfit to known vocabulary.

### SL-084: Wrong-Tier Labeled Examples Should Feed DSPy Before Keyword Expansion — 2026-04-11
<!-- meta: { "run_id": "SL084_dspy_before_keywords", "domain": "classifier/training", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "staleness_check": "2026-07-11" } -->

**Finding**: When keyword tuning fails 3+ consecutive rounds on the same failure class, those failures are the BEST DSPy training examples. Stop tuning keywords, start accumulating labeled data.
**Evidence**: Brain audit 2026-04-11: 3 prompts persisted wrong after 4 keyword rounds. DSPy selected all 3 as few-shot demos automatically (BootstrapFewShot metric-driven selection). LLM fallback now routes them correctly.
**Applies to**: brain, godspeed, ALL classifier workflows
**Action**: Track "consecutive-round failures." If same prompt fails 3+ rounds → tag as DSPy priority training example, stop adding keywords for that class.

### Anti-Pattern: Tier boundary changes require guardrail min_score audit — SL-085 — 2026-04-12
<!-- meta: { "run_id": "brain_guardrail_drift_20260412", "domain": "toke", "confidence": "HIGH", "confirmed_count": 2, "roi_score": 5, "staleness_check": "2026-07-12" } -->

**Finding**: When Brain tier thresholds (s3_max, s4_max) are adjusted, existing guardrail min_score values silently diverge. A guardrail labeled "S4 floor" with min_score=0.80 routes S5 when s4_max=0.55. Caused 30/32 over-routing events.
**Evidence**: Confusion matrix 2026-04-12: Brain S5 accuracy 9.1% — 30 of 33 wrong S5 decisions traced to miscalibrated guardrails (architecture_work, multi_file_refactor, creative_game_design).
**Applies to**: brain, godspeed, aurora
**Action**: After any threshold change, audit ALL min_score values in routing_manifest.toml. Verify each falls in its labeled tier range: S4=[s3_max, s4_max), S5=[s4_max, 1.0]. Systemic grep, not manual review.

### Anti-Pattern: Project-context-aware guardrails prevent cross-domain false positives — SL-087 — 2026-04-12
<!-- meta: { "run_id": "brain_cwd_domain_guardrails_20260412", "domain": "toke", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-07-12" } -->

**Finding**: Keyword-based classifier guardrails fire on domain-specific terms (e.g., "your project", "UE5") even when the user is discussing those domains from within a different project's context (meta-tasks, cross-project references). This causes false positives that over-route by 1-2 tiers.
**Evidence**: Brain v2.4: "verify your project combat and check MyActor.h" with CWD=Toke routed S5 (ue5_code_work guardrail fired). With domain_tags=["ue5"] on that guardrail, same prompt routes S3. Fix confirmed by 10/10 v2.4 tests.
**Applies to**: brain, godspeed, ALL
**Action**: Tag project-specific guardrails with `domain_tags = ["project_name"]` in the manifest. Classifier detects CWD → project domain, suppresses mismatched guardrails. Manifest stays single source of truth — no Python hard-coding. Pattern extends to any domain-specific guardrail (your-trading-project, your-3d-app, etc.).

### Anti-Pattern: Infra items belong to the sprint that needs them, not Sprint 0 — SL-088 — 2026-04-11
<!-- meta: { "run_id": "godspeed_sprint0_reassessment_20260411", "domain": "ALL", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "staleness_check": "2026-07-11" } -->

**Finding**: Gap audits and blueprints evaluated from a "ready to ship" lens over-assign infra items to Sprint 0 when most only matter at the sprint that first uses them.
**Evidence**: your game project Sprint 0 had 10 "emergency" items. 8 were premature for a solo dev using Toke session memory. Only 2 actually blocked development (INI merge + AssetManager types = 30 min). Collision profiles, physics surfaces, gameplay tags, packaging config, RepGraph expansion — all tied to Sprint 2-5 systems that don't exist yet.
**Applies to**: godspeed, blueprint, holy-trinity, ALL skills that generate gap audits or execution plans
**Action**: For each infra item in a blueprint, ask: "Does this block the NEXT sprint specifically, or does it block SHIPPING?" If shipping → assign to the sprint where the dependent system gets built. Solo devs with session-memory tooling (Toke) have different urgency profiles than team projects. Git is "slow-day task" not "Day 1 emergency" when session memory tracks changes.

### Anti-Pattern: Fail-silent hooks require error log — SL-086 — 2026-04-12
<!-- meta: { "run_id": "hook_silent_failure_20260412", "domain": "toke", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-07-12" } -->

**Finding**: Hooks that swallow exceptions silently (exit 0 on any error) produce zero signal when they fail. A Python→JS regex port bug ((?i) inline flag invalid in JS) caused 8 consecutive silent failures — correct latency, exit 0, no JSONL writes, no stderr.
**Evidence**: brain_hook_fast.js exited 0 on every call but wrote nothing until hook_errors.log was added, which immediately revealed `Invalid regular expression: /(?i)\bdesign\b/is: Invalid group`.
**Applies to**: brain, godspeed, ALL hook scripts
**Action**: Every fail-silent hook MUST write errors to a dedicated log file (e.g., hook_errors.log) before swallowing. Pattern: `catch(e) { appendFileSync(errLog, ...) ; exit(0) }`. Zero-output + exit-0 is indistinguishable from success without a log.

### INSIGHT: Ceiling guardrails recover tier collapse after evolutionary optimization — SL-089 — 2026-04-12
<!-- meta: { "run_id": "ceiling_guardrail_tier_recovery_20260412c", "domain": "toke", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "staleness_check": "2026-07-12" } -->

**Finding**: GEPA evolutionary optimization of classifier thresholds caused S2 tier to completely collapse (17/17 → 0/17 exact) because floor guardrails (min_score=0.22) now equaled s2_max (0.22), pushing all S2 prompts to S3. Fix: add a `ceiling_guardrails` mechanism (max_score) processed AFTER floors, capping score when specific-code-reference patterns are detected. Recovered 16/17 S2 prompts. Net: +27 exact this session (53%→66.5%), 0.828 weighted.
**Evidence**: eval_golden_set_v2.6_final2_2026-04-12c.json — 133/200 exact, 2 wrong, 42/42 tests. File-extension patterns (.py, .jsonl) caused 17 S3/S4/S5 false positives and were unsafe. Narrow patterns (function(), "the X function", "this file", docstrings, CLI flags) were safe.
**Applies to**: brain, godspeed, ALL classifier systems
**Action**: When evolutionary/threshold optimization collapses a tier, add ceiling_guardrails with NARROW specificity patterns (not broad file extensions). Test by running full eval after every pattern addition — one bad pattern causes cascading wrong routes. Pattern: floor guardrails push UP (min_score), ceiling guardrails push DOWN (max_score), ceilings always process after floors.


### SL-090: Re-inspect before executing greenlit destructive actions — narrow scope when new info surfaces risk
<!-- meta: { "id": "SL-090", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 5, "applies_to": "ALL", "staleness_check": "2026-04-16", "source_tier": "T4" } -->

**Finding**: When the user greenlights a destructive action (file/dir delete, truncate, force-push, etc.), the correct protocol is NOT to execute blindly — it is to RE-INSPECT the target one more time, and if new information reveals risk that wasn't visible at greenlight time, NARROW THE SCOPE and surface the narrowing to the user in the report. Blind execution of a greenlit action when new info invalidates the greenlight's premise is worse than pausing.

**Evidence**: 2026-04-16 Your-Automation-Skill cleanup campaign. I proposed deleting `~/.claude/projects/C--project-memory/` as "stale pre-T1 memory project (dangling pointer)". the user greenlit. Pre-execution inspection (`ls -la`) revealed the dir contained not just 4 stale memory `.md` files but ALSO 3 session UUID conversation JSONL logs from Mar 28-29 — real Claude Code historical conversation data, not stale memory. Blind execution of the greenlit `rm -rf` would have destroyed historical conversation records. Narrowed scope to delete only the 4 `.md` files + the now-empty `memory/` subdir. Session UUID logs preserved. Narrowing flagged to the user in the report under a "Scope Narrowing" header.

**Applies to**: ALL skills that execute destructive actions on user greenlight — godspeed cleanup proposals, devTeam refactors, debug fix-and-delete patterns, organizer dir reshuffles, close-session memory writes, any skill that calls `rm`/`git reset --hard`/`force-push`/`DROP TABLE`.

**Action**: 
1. Before executing any greenlit destructive action, do a final `ls`/`cat`/`grep` inspection of the target.
2. If inspection surfaces content that wasn't visible when the proposal was made — STOP.
3. Evaluate: does the new info change the scope? (E.g. "I proposed deleting a dir, but now I see it contains files not part of the proposal's justification.")
4. If yes — narrow the scope to what actually matches the original proposal's intent (the 4 stale `.md` files in the example, not the whole dir).
5. Execute the narrowed action.
6. REPORT the narrowing prominently under a "Scope Narrowing" or similar header. Do NOT bury it in the success log. the user needs to see that you deviated from the literal greenlight and why.

**Why it works**: Sacred Rule #1 (truthful) + Sacred Rule #2 (never delete without consent) interact here. The greenlight was consent for the PROPOSAL, not for anything inside the target. If new info invalidates the proposal's premise, the consent is stale — narrow scope to match what was actually consented to, and re-surface to the user.

**Why it matters**: Historical data loss from blind `rm -rf` on greenlit dirs is a silent disaster that surfaces weeks later when the user tries to retrieve old context. Pausing for 60 seconds to inspect + narrow costs nothing; executing blindly can cost irreplaceable work history.

**Cross-reference**: Extends Sacred Rule #2 (never delete without consent). Extends godspeed v4.3 "deletion proposals only — never unilateral deletes" rule. Complements SL-080 (research-before-3rd-iteration — another pause-and-inspect pattern).
