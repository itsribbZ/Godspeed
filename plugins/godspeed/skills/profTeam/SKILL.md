---
name: profTeam
description: >
  Adaptive multi-agent parallel research engine. Deploys agent configurations based on topic
  classification and accumulated ROI data. Cross-validates with confidence matrix. Smart Cycle
  compression. Failure recovery. Output: ONE master Blueprint PDF. Holy Tool status.
model: opus
effort: high
---

# ProfTeam v4.0 — Adaptive Multi-Agent Research & Refinement Engine

## Pipeline Overview
Phase 0 (Classify + Pre-flight) → Phase 1 (Deploy Adaptive Agents, parallel) → Phase 1.5 (Validate + Recover) → Phase 2 (Cross-Reference + DevTeam Gate) → Phase 3 (Beta PDFs) → Phase 4 (Smart Cycle) → Phase 5 (Master PDF) → Phase 6 (Learnings + ROI)

## When to Trigger

- User says "profTeam", "deploy profTeam", "run profTeam", "use profTeam on [topic]"
- User says "deep research", "heavy research", "comprehensive research"
- User says "multi-agent research on [topic]"
- A topic is too large or too critical for a single Professor pass
- When the Holy Trinity's Phase 2 targets profTeam with specific diagnostic gaps

## Topic Classification Engine (v2.0)

Before deploying agents, classify the topic to auto-select the optimal agent configuration. Classification is based on the topic + accumulated ROI data from `_learnings.md`.

### Topic Types & Default Agent Configs

| Topic Type | Detection Signal | Default Agents | Mandatory | Optimal Count |
|-----------|-----------------|----------------|-----------|---------------|
| **Architecture** | "system", "design", "component", "architecture" | A:Theory, B:UE5/Impl, C:Industry, D:Pitfalls, F:CrossSystem | D | 5 |
| **Debugging** | "bug", "fix", "broken", "not working", specific error | A:Theory, B:Impl, D:Pitfalls, E:Codebase | D, E | 4-5 |
| **Performance** | "fps", "optimize", "memory", "draw calls", "lag" | A+C:Merged(Theory+Industry), B:Impl, D:Pitfalls, E:Codebase | D | 4 |
| **Game Design** | "gameplay", "mechanic", "combat feel", "player experience" | A:Theory, C:Industry, D:Pitfalls, E:Experimental | D | 4-5 |
| **Product/Business** | "market", "competition", "revenue", "pricing" | A:Market, B:Users, C:Tech, D:Pitfalls, E:Growth | D | 5-6 |
| **Networking** | "multiplayer", "replication", "server", "sync" | A:Theory, B:UE5Net, C:Industry, D:Pitfalls, E:Security | D | 5 |
| **Broad/Unknown** | Cannot classify | A:Theory, B:Impl, C:Industry, D:Pitfalls | D | 4 |

### Adaptive Overrides (from learnings)

Before finalizing agent config, check `_learnings.md` for ROI data on similar past topics:
1. If a topic type has been run before → use the "Optimization for Next Run" from that entry
2. If Agent D was MVP in a similar run → increase its search budget (8-10 queries)
3. If two agents overlapped in a similar run → merge them per the optimization note
4. If Agent E (Codebase) found root causes in a similar run → promote to mandatory

## Project Context
Project-agnostic. Paths loaded dynamically:
- **UE5/your project**: Docs and PDF output detected from project init
- **SaaS**: Output to project `docs/research/`
- **Any other**: PDF output defaults to project root + `/docs/research/`
Specific paths come from project init skills, NOT hardcoded here.

**Pre-work**: Follow _shared_protocols.md S1.

## Workflow

### Phase 0: Load Learnings, Classify Topic & Select Config

1. **Read `_learnings.md`** — accumulated insights from previous runs
2. **Read `.claude/shared/_shared_learnings.md`** — cross-skill learnings
3. **Parse the user's prompt** to extract:
   - **Topic**: What to research
   - **Scope**: How broad (single system vs ecosystem)
   - **Urgency**: Immediate implementation or long-term planning?
4. **Classify topic** using the Topic Classification Engine
5. **Select agent config** from the classification table + adaptive overrides from learnings
6. **Check existing research**: Search docs/research folders and project docs for prior work. ProfTeam EXTENDS — never starts from zero.
7. **Report config to user**: "Classified as [type]. Deploying [N] agents: [list with focuses]"

### Phase 0.5: Initialize Infrastructure

#### Checkpoint Setup
1. **Generate session ID**: `profteam_[topic_slug]_[YYYYMMDD_HHMMSS]`
2. **Set CHECKPOINT_DIR**: `[docs_root]/Research/.profteam_checkpoints/[session-id]/`
3. **Create directory** via Bash: `mkdir -p "[CHECKPOINT_DIR]"`
4. **Write initial manifest.json** with agent list, statuses, timestamps
5. **Log to user**: "Checkpoint infrastructure initialized at [CHECKPOINT_DIR]"
6. **Compaction survival marker**: `PROFTEAM SESSION: [session-id] | CHECKPOINT: [CHECKPOINT_DIR]`

#### Context Budget Estimation (v4.0)
Before deploying agents, estimate total context cost to prevent compaction:

1. **Count pre-flight context**: project docs (~500 lines each), existing PDFs (~300 lines each), source files
2. **Count agent budget**: [N agents] × [avg 500 words return] + checkpoint overhead
3. **Count cross-reference**: All agent findings merged (~200 lines per agent)
4. **Count PDF generation**: Generator script (~300 lines) + output verification
5. **Total estimate**: Sum all above. Report: "Context budget estimate: ~[X]K tokens"
6. **If estimate > 60% of context window**:
   - Reduce agent count (merge lowest-ROI agents)
   - Summarize pre-flight context instead of loading in full
   - Use Sonnet agents for self-contained research (14x faster, less context)
   - Report: "Context pressure HIGH — [action taken to reduce]"
7. **If estimate ≤ 60%**: proceed normally

#### Pre-Flight Context Gathering (v4.0)
Before deploying agents, gather context that makes agent prompts more targeted:
1. **If debugging topic**: Read the actual source files related to the bug (Agent E gets these too, but all agents benefit from context)
2. **If architecture topic**: Run Explore agent to map relevant modules, scan project docs
3. **If extending existing system**: Grep for existing patterns, interfaces, data contracts
4. **Inject gathered context** into every agent's prompt as "EXISTING CONTEXT" section
5. **project docs Pre-Load Mandate (v3.0)**: For your project or any UE5/game code topic — read the directly relevant project docs(s) BEFORE deploying agents. Per SL-004 (HIGH confidence, 7+ runs validated): project docs provide 90%+ of needed architectural context and outperform web searches. Inject project docs content into ALL agent prompts as "PROJECT-DOCS CONTEXT". Any web search that duplicates what project documentation already covers is wasted budget — skip it.
   - Architecture/Code topic → project reference docs mandatory
   - Game system topic → relevant project docs for that system
   - Performance topic → project reference docs + Ch.13
   - All topics → project reference docs as supplement
6. **Existing Research Pre-Load (v3.0)**: Per SL-005 (HIGH confidence, 7+ runs validated) — check `Docs/Design Systems/Research/` for existing PDFs on the topic BEFORE agents begin web searches. Load found PDFs as "PRIOR RESEARCH" context in agent prompts. Existing research covered 80-90% of content in multiple runs — agents EXTEND, they do not duplicate. Report: "Prior research found: [N] PDFs. Agents targeting gaps and updates only."

### Phase 1: Deploy Adaptive Agents

Deploy agents in parallel using the config from Phase 0. Each agent is a specialized research instance.

**Parallel dispatch**: Follow _shared_protocols.md S3. ALL agents in ONE message — no exceptions. Only deploy sequentially if Agent B genuinely requires Agent A's specific output as input.

#### Agent Specializations (adapted per topic type)

| Agent | Focus | Source Priority |
|-------|-------|-----------------|
| **Agent A: Core Theory** | Foundational concepts, academic research, design patterns | Academic papers, GDC talks, textbooks |
| **Agent B: Implementation** | Engine/framework APIs, code patterns, documentation | Official docs, engine source, technical blogs |
| **Agent C: Industry Practice** | How studios/teams solve this, shipped examples, postmortems | GDC postmortems, studio blogs, benchmarks |
| **Agent D: Pitfalls & Edge Cases** | What goes wrong, performance traps, scaling issues, anti-patterns | Bug reports, performance analyses, community pain points |
| **Agent E: Codebase Analysis** | Read actual source files, trace data flow, identify root causes | The actual project source code |
| **Agent F: Cross-System** | Integration points, data flow across system boundaries | project docs, existing codebase, architecture docs |

#### Dynamic Agent Extension (v4.0)

The A-F roster is a STARTING SET, not a cap. When a topic requires specialization beyond the default 6:

1. **Auto-create Agent G+** when:
   - A topic spans 3+ distinct sub-domains that don't fit existing agent focuses
   - The Adaptive Config Engine identifies a gap that no existing agent covers
   - User explicitly requests a specialized agent focus
2. **Naming**: Agent G: [Focus], Agent H: [Focus], etc.
3. **Budget**: New agents get 5 searches by default (standard tier). Promote to 8-10 after first run if ROI ≥ 4/5.
4. **Lifecycle**: Dynamic agents persist in ROI Leaderboard. If a dynamic agent achieves ROI ≥ 4/5 across 3+ runs, promote it to the permanent roster with a letter designation.
5. **Cap**: Maximum 8 agents per run. Beyond 8, merge the two lowest-ROI agents instead of adding.
6. **Report**: "Dynamic agent created: Agent G: [Focus] — reason: [gap/user request/sub-domain]"

#### Agent Rules (ALL agents must follow)

1. **Verified sources ONLY** — Source tiers and Verified Data Floor: see _shared_protocols.md S2.
2. **5-8 web searches per agent** (Agent D gets 8-10 if high-ROI history)
3. **Structured output**: key findings, confidence levels, code patterns, contradictions, cross-validation questions
4. **Model selection (v2.1 DEFAULT per SL-062)**: Research agents A-F use **Sonnet** by default — 14× faster, ~1% quality delta per empirical SL from 2026-04-04. Use **Opus** ONLY for: (a) Phase 2 Cross-Reference synthesis (multi-agent fusion is judgment-heavy), (b) DevTeam gate scoring (architecture evaluation needs Opus precision), (c) any agent working on a topic flagged regression-critical by holy-trinity. Previous v4.0 behavior used Sonnet only under context pressure — v2.1 flips this: Sonnet is the baseline, Opus is opt-in. Expected: ~5× cost reduction on research passes with no measurable quality loss.
5. **Prompt cache ordering (v2.1 per §12)**: Build each agent prompt top → bottom as invariant (tool list, 7 Laws, source tiers, PROVEN QUERIES) → semi-stable (domain context, skill contracts, filtered learnings) → volatile (topic, per-run gaps). Never interleave volatile into invariant blocks.

#### Checkpoint Requirement

Every agent prompt MUST include:
```
CHECKPOINT: When you complete your research, you MUST write your structured findings to:
  [CHECKPOINT_DIR]/Agent_[X]_results.json
Format: {"agent": "[X]", "focus": "[focus]", "findings": [...], "sources": [...], "confidence": {...}, "roi_self_assessment": [1-5]}
Also write a 200-word summary to: [CHECKPOINT_DIR]/Agent_[X]_summary.md
THEN return your findings as a COMPACT numbered list (max 500 words).
Your DETAILED analysis goes in the checkpoint file. Return only the executive summary.
```

### Phase 1.5: Incremental Collection, Validation & Loss Recovery

As each agent returns:
1. **Validate agent output** (v2.1 — see Agent Output Validation below)
2. **Verify checkpoint file exists** on disk. If not, extract from inline results and write it.
3. **Update manifest.json** with completion timestamp and agent's ROI self-assessment.
4. **Begin cross-referencing** incrementally with previously completed agents.

#### Agent Output Validation (v2.1 — Reliability → 5/5)

Every agent's output is validated before acceptance:

**Required Fields Check:**
- [ ] At least 3 numbered findings (generic/empty returns fail)
- [ ] Each finding has a confidence tag (HIGH/MEDIUM/LOW)
- [ ] At least 1 source citation with tier tag (Tier 1-5)
- [ ] ROI self-assessment score (1-5)
- [ ] No Tier 5-only findings without higher-tier corroboration

**Quality Floor Check:**
- [ ] Findings are specific to the topic (not generic advice)
- [ ] At least 1 finding references concrete API, function, or technique
- [ ] No contradictions within a single agent's output

**If validation fails:**
1. Classify failure: EMPTY (< 3 findings) | GENERIC (no specifics) | UNSOURCED (no tier tags)
2. For EMPTY/GENERIC: Re-deploy agent with tighter prompt + other agents' findings as context
3. For UNSOURCED: Accept findings but downgrade all to UNVERIFIED in confidence matrix
4. Log: "Agent [X] output validation failed: [type]. Action: [retry/downgrade]"
5. Max 1 retry per agent — if second attempt fails, proceed without that agent

#### Failure Recovery Catalog (v4.0 — Auto-Recovery)

| Failure Mode | Detection | Recovery |
|-------------|-----------|----------|
| **Agent lost to compaction** | manifest shows "deployed" but no checkpoint + no inline return | **AUTO-RECOVER v4.0**: Read manifest.json → identify lost agents → read checkpoint files from surviving agents → re-deploy ONLY lost agents with surviving findings as context. No manual intervention needed. |
| **Agent returns empty/generic** | Findings are <3 or all UNVERIFIED | Re-deploy with tighter prompt + existing agents' specific findings |
| **Checkpoint dir inaccessible** | mkdir fails or write permission denied | Fall back to inline-only mode, warn user |
| **All agents agree but shallow** | All VERIFIED but <5 findings total | Deploy 1-2 additional agents with deeper focus |
| **Agent contradicts all others** | 1 vs N disagreement | Investigate: check source tiers. If lone agent has Tier 1 source, it may be correct. Present both. |
| **Context compaction mid-run** | Lost track of which agents returned | **AUTO-RECOVER v4.0**: Read manifest.json + ALL checkpoint files → reconstruct complete state → resume from last completed phase. Report: "Auto-recovered from compaction. [N] agents recovered from checkpoints." |
| **Partial agent results** | Agent returned but checkpoint is incomplete | Extract inline results → write to checkpoint → proceed with partial data flagged |

#### Auto-Recovery Protocol (v4.0)

When ANY recovery event fires:
1. **Read manifest.json** — determine which agents completed, which are lost
2. **Scan checkpoint dir** — read all `Agent_*_results.json` and `Agent_*_summary.md` files
3. **Reconstruct state** — build unified findings list from checkpoint data
4. **Identify gaps** — which agents' findings are missing?
5. **Re-deploy lost agents ONLY** — include surviving agents' findings as "EXISTING CONTEXT" in prompts
6. **Log recovery event** — append to `_learnings.md`:
   ```
   ### Recovery Event: [Topic] — [Date]
   - Lost agents: [list]
   - Recovered from checkpoint: [list]  
   - Re-deployed: [list]
   - Recovery time: ~[N] minutes
   - Data loss: [none / partial — details]
   ```
7. **Update manifest.json** with recovery status

### Phase 2: Cross-Reference & Validate (with DevTeam Gate)

After all agents return:

1. **Compile all findings** into unified dataset
2. **DevTeam Architecture Filter** — run devTeam v4.0's 7 Laws against all proposed patterns. Flag any finding that violates Laws 1-7 BEFORE it enters the confidence matrix
3. **Resolve contradictions**:
   - Which agent has higher-tier sources?
   - Is the contradiction contextual (e.g., single-player vs MMO)?
   - Can both be true in different scenarios?
   - **DevTeam tiebreaker**: If sources are equal, devTeam's Fluidity Checklist determines architectural superiority
4. **Validate key claims** — every HIGH-confidence finding must appear in 2+ agents' results
5. **Merge overlapping findings** — deduplicate, preserve strongest citations
6. **DevTeam Complexity Audit** — score all proposed implementations for CC, CBO, anti-pattern risk
7. **Identify gaps** — what did NO agent cover?
8. **Build Confidence Matrix**:
   - **VERIFIED** (3+ agents agree, Tier 1-3 sources) → proven
   - **PROBABLE** (2 agents agree, mixed sources) → include with caveats
   - **UNVERIFIED** (single agent, Tier 4-5 sources) → flag for Cycle
   - **CONTRADICTED** (agents disagree) → present both sides

### Phase 3: Compile Beta PDFs

Organize validated findings into 3 beta PDFs:

- **Beta 1: Foundation** — Core concepts, established patterns, "everyone agrees" baseline (Agent A + C)
- **Beta 2: Implementation** — APIs, code patterns, integration, performance (Agent B + D)
- **Beta 3: Advanced** — Experimental, edge cases, cross-system, future-proofing (Agent E + F)

Beta PDFs are intermediate input for the Cycle engine — not final deliverables.

### Phase 4: Smart Cycle (v2.0 — Adaptive Compression)

#### Compression Decision Engine

Before running Cycle, evaluate whether full 3-pass is needed:

```
IF (contradictions == 0) AND (verified_ratio >= 0.90) AND (total_findings >= 15):
    → COMPRESS: Run single synthesis pass (skip Cycles 2-3)
    → Rationale: Strong consensus, minimal gaps to fill

ELIF (contradictions <= 2) AND (verified_ratio >= 0.75):
    → PARTIAL: Run 2 passes (skip Cycle 3)
    → Rationale: Minor gaps, one refinement sufficient

ELSE:
    → FULL: Run all 3 Cycle passes
    → Rationale: Significant gaps or contradictions need iterative resolution
```

Report the compression decision: "Consensus is [strong/moderate/weak]. Running [1/2/3] Cycle pass(es)."

#### Cycle Passes (when running)

**Cycle 1: Foundation Pass**
- Input: All beta PDFs + validated cross-reference data
- Blueprint scan: Existing codebase, project docs, research docs
- Output: Raw inventory + gap analysis + initial architecture
- Then: DevTeam fluidity analysis → Professor targeted research on gaps

**Cycle 2: Refinement Pass** (if not compressed)
- Input: Cycle 1 output + DevTeam findings + Professor research
- Deepens: Specific class designs, phased implementation, risk scoring
- Replaces: Outdated info from beta PDFs with fresher data
- Then: DevTeam re-score → Professor fills remaining gaps

**Cycle 3: Synthesis Pass** (if full)
- Input: Cycle 2 output + all accumulated knowledge
- Produces: Final comprehensive blueprint with all 14 sections
- Then: Final DevTeam audit and score comparison across all cycles

### Phase 5: Master PDF Compilation

Generate ONE master Blueprint PDF using Bifrost:

```python
import sys, os
# Resolve BifrostPDF path dynamically — check known locations in order
for bifrost_path in [
    os.path.expanduser(r"~\Desktop\your project721\Tools\BifrostPDF"),
    os.path.expanduser(r"~\Desktop\T1\Tools\BifrostPDF"),
    os.path.join(os.getcwd(), "Tools", "BifrostPDF"),
]:
    if os.path.isdir(bifrost_path):
        sys.path.insert(0, bifrost_path)
        break
from bifrost_pdf import BifrostPDF, BifrostTheme as T

pdf = BifrostPDF(
    title="[Topic] — ProfTeam Master Blueprint",
    subtitle="Multi-Agent Research + Adaptive Cycle Refinement",
    output_path=r"[docs_root]\Research\ProfTeam_[Topic].pdf",
    footer="ProfTeam v4.0 // Master Blueprint // [Topic]"
)
```

**14 Sections** (from Cycle output):
1. Executive Summary
2. Existing System Audit
3. Architecture Design
4. Dependency Matrix
5. Phased Implementation Roadmap
6. Data Architecture
7. Performance Budget (threshold-colored)
8. Technical Risk Assessment
9. DevTeam Fluidity Audit (v2.0 — with calibrated scoring)
10. ProfTeam Research Summary (confidence matrix, agent contributions)
11. Source Quality Report (all citations with tier badges)
12. Optimization Recommendations
13. Priority Matrix (impact × effort)
14. Cycle Evolution Log (compression decision + pass improvements)

Save generator script and output PDF to project docs folder.

### Phase 5.5: PDF Output Validation (v4.0)

Before declaring the master PDF complete, validate its structure:

#### Required Sections Checklist
- [ ] All 14 sections present (check section headers in generator script)
- [ ] Executive Summary is ≤1 page (concise, not bloated)
- [ ] At least 1 code example in Architecture Design or Implementation sections
- [ ] Confidence matrix included in ProfTeam Research Summary
- [ ] Source Quality Report has ≥1 T1-T3 citation per VERIFIED finding
- [ ] Priority Matrix has ≥3 entries ranked by impact × effort
- [ ] Cycle Evolution Log documents compression decision + rationale

#### Quality Floor Checks
- [ ] Total findings ≥ 10 (below this = research was too shallow)
- [ ] Verified ratio ≥ 50% (below this = insufficient source quality)
- [ ] No section is empty or contains only placeholder text
- [ ] Page count ≥ 5 (below this = content too thin for a "master blueprint")

#### Regression Check (if previous PDF exists on same topic)
- [ ] Section count ≥ previous PDF's section count
- [ ] Finding count ≥ previous PDF's finding count (EXTEND, never shrink)
- [ ] No sections removed that existed in previous version

#### If Validation Fails
1. Identify which checks failed
2. For missing sections: check if beta PDFs or agent checkpoints contain the content — extract and add
3. For quality floor: re-deploy targeted agents to fill gaps
4. For regression: restore missing sections from previous PDF
5. Log: "PDF validation failed: [checks]. Action: [fill/restore/redeploy]"
6. Max 1 re-generation attempt — if second attempt fails, deliver with `[INCOMPLETE]` tags on failed sections

### Phase 6: Record Learnings + Agent ROI (v4.0)

Append to `_learnings.md` after every run:

```markdown
## Run: [Topic] — [Date] — Type: [classified type]

### Agent Config
| Agent | Focus | Searches | Findings | ROI (1-5) | MVP? |
|-------|-------|----------|----------|-----------|------|
| A | [focus] | N | N | X | |
| D | [focus] | N | N | X | * |

### ROI Analysis
- **MVP Agent**: [which] — [why]
- **Lowest ROI Agent**: [which] — [why] — **Optimization**: [merge/cut/retarget]
- **Agent overlap detected**: [agents] on [topic] — **Next time**: [merge strategy]

### Cross-Reference Results
- Verified: [N] (3+ agents, Tier 1-3)
- Probable: [N] (2 agents)
- Unverified: [N] (single-source)
- Contradicted: [N] (disagreements)

### Cycle Compression Decision
- Decision: [COMPRESS/PARTIAL/FULL]
- Rationale: [contradictions=N, verified_ratio=X%, findings=N]
- Correct? [Yes/No — was compression appropriate or did we miss gaps?]

### What Worked
- [specific techniques, queries, agent configs that were productive]

### What Was Slow
- [bottlenecks, low-value angles, redundant work]

### Failure Recovery Events
- [any agent losses, checkpoint issues, recovery actions taken]

### Optimization for Next Run (CRITICAL — future runs read this)
- [specific improvements for similar topic types]

### Output
- PDF: [path]
- Pages: [N] | Sections: [N] | Size: [X KB]
- Generator: [path]
```

### Calibration Echo — Topic Classification Accuracy (v2.1 per SL-062)

Close the self-improvement loop on topic classification. Track whether profTeam's topic type classification (Phase 0) correctly predicted the agent config that delivered MVP findings. Mirrors devTeam v4.0 Calibration Echo pattern.

**Protocol**:
1. **Before Phase 1 dispatch**: record the classified topic type + predicted MVP agent(s) from ROI Leaderboard
2. **After Phase 6 ROI scoring**: record the ACTUAL MVP agent(s) based on delivered findings
3. **Compute accuracy**: did the predicted MVP agent match the actual?
4. **Write IMMEDIATELY per §5** to `_learnings.md`:
   ```
   ### Calibration Echo: Classification — [Topic Type] — [Date]
   <!-- meta: { "run_id": "profteam_echo_[type]_[date]", "domain": "skills", "confidence": "HIGH", "confirmed_count": 1, "roi_score": 4, "staleness_check": "[date]" } -->
   - Classified as: [type] | Predicted MVP: Agent [X] | Actual MVP: Agent [Y]
   - Match: Y/N
   - Running accuracy: [X]% over last 5 runs of [type]
   - Status: WELL-CALIBRATED (>66%) | DEVELOPING (33-66%) | MISCALIBRATED (<33%)
   - Adjustment: [none / promote Agent Y for type / demote Agent X for type]
   ```
5. **If MISCALIBRATED for a topic type across 3+ runs**: update the Topic Classification Engine default agent config for that type. Shift MVP predictions toward agents with empirical ROI track record.

This closes the loop. Topic classification gets smarter with every profTeam run. Over 10+ runs per topic type, classification develops topic-specific expertise that drives auto-config without user intervention.

## Agent ROI Tracking (v2.0 — Cumulative)

ProfTeam maintains cumulative ROI data across all runs. After 5+ runs, the ROI data becomes highly predictive:

### ROI Leaderboard (from learnings)
When reading `_learnings.md`, compute per-agent-type average ROI across all runs:
- **Agent D (Pitfalls)**: Consistently highest ROI (4/5 runs MVP). ALWAYS deploy. Budget: 8-10 searches.
- **Agent E (Codebase)**: Highest ROI for debugging topics (2/2 MVP). MANDATORY for debugging.
- **Agent A (Theory)**: High baseline value but overlaps with Agent C on some topics. Consider merging for performance topics.
- **Agent B (Implementation)**: Steady value, rarely MVP but consistently useful. Keep.
- **Agent C (Industry)**: High creative value. Most useful for design topics. Overlaps with A for performance.
- **Agent F (Cross-System)**: Niche value. Deploy only when topic spans multiple systems.

Update this leaderboard after every run based on actual ROI scores.

## Calibration Feedback
After every run, profTeam feeds back to devTeam: which Laws were most relevant, agent ROI per topic type. Write calibration entries to devTeam's _learnings.md and shared learnings for cross-skill use.

## Research Cache
Before deploying agents, scan existing checkpoint dirs for same topic slug. Cache hit → agents target GAPS and UPDATES only, skip duplicate queries. Cache >90 days old → verify rather than trust.

## Query Learning Engine (v4.0 — Self-Improving Searches)

Track which search queries produce high-ROI results to improve future agent prompts.

### After Each Agent Returns
1. **Extract query list** — which searches did the agent run?
2. **Score each query**: 
   - Produced a VERIFIED finding → `ROI: HIGH`
   - Produced a PROBABLE finding → `ROI: MEDIUM`
   - Produced nothing actionable → `ROI: LOW`
3. **Append to _learnings.md** under the run entry:
   ```
   ### Query ROI: [Agent] — [Topic Type]
   | Query | ROI | Finding Produced |
   |-------|-----|-----------------|
   | "[query text]" | HIGH | [brief finding] |
   | "[query text]" | LOW | nothing actionable |
   ```

### Before Deploying Future Agents
1. **Read previous Query ROI tables** for the same topic type
2. **Inject HIGH-ROI query patterns** into agent prompts as "PROVEN QUERIES — prioritize these patterns"
3. **Flag LOW-ROI patterns** as "AVOID — these patterns produced nothing in [N] previous runs"
4. **Report**: "Query learning applied: [N] proven patterns injected, [M] anti-patterns flagged"

Over time, agents develop topic-type-specific query expertise. Architecture queries learn which GDC talk phrasings work. Debugging queries learn which error-pattern phrasings find root causes.

## Adaptive Agent Config Engine (v4.0 — Fully Automatic)

Agent config selection is now FULLY data-driven from ROI leaderboard. No manual override needed.

### Auto-Config Protocol
1. **Read ROI Leaderboard** from `_learnings.md` header
2. **For the classified topic type**, look up historical agent configs + their ROI scores
3. **Auto-select agents**:
   - Always include agents with ROI ≥ 4/5 for this topic type
   - Merge agents with >50% finding overlap in previous runs of same type
   - Drop agents with ROI ≤ 2/5 for 2+ consecutive runs of same type (replace with higher-ROI alternative)
   - Agent D (Pitfalls): ALWAYS deployed regardless of topic type (proven 5/5 ROI across all runs)
4. **Auto-adjust search budgets**:
   - ROI ≥ 4/5 agents: 8-10 searches
   - ROI 3/5 agents: 5-7 searches
   - ROI ≤ 2/5 agents: 3-5 searches (if deployed at all)
5. **Report config rationale**: "Auto-config: [N] agents selected. [Agent X] promoted (ROI 5/5 in [type]). [Agent Y] merged with [Agent Z] (>50% overlap in previous run)."

### ROI Leaderboard Auto-Update
After Phase 6 learning write, automatically recompute the cumulative ROI leaderboard at the top of `_learnings.md`. This is the SINGLE SOURCE OF TRUTH for agent config decisions.

**Incremental checkpoints**: Follow _shared_protocols.md S5. ProfTeam writes after each agent returns, after cross-reference, and after compression decision.

## Protocols

Follow `${CLAUDE_PLUGIN_ROOT}/shared/_shared_protocols.md` for: pre-work loading, source tiers, parallel execution, post-invocation learning, incremental checkpoints, session safety, structured learning format, cross-skill auto-promotion, staleness detection.
