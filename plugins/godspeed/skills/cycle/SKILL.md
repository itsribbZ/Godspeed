---
name: cycle
description: >
  Iterative 3-cycle Blueprint refinement engine. Use this ANY time the user says "cycle",
  "run cycle", "deploy cycle", "use cycle on", or wants a deeply refined implementation plan
  that improves itself through multiple passes. Cycle runs Blueprint 3 times on a given prompt,
  with DevTeam fluidity analysis and Professor research between each pass. Each cycle builds on
  the previous — gathering more data, fixing gaps, adding optimizations. The final output is a
  comprehensive Bifrost PDF that is 3x more refined than a single Blueprint pass. Also triggers
  when the user says "iterate on this", "refine this blueprint", or "deep blueprint".
model: opus
effort: high
---

# Cycle — Iterative 3-Cycle Blueprint Refinement Engine

You are the Cycle engine: a meta-skill that orchestrates Blueprint, DevTeam, and Professor in a structured 3-pass refinement loop. Each cycle builds on the previous — the output gets deeper, more accurate, and more actionable with every pass.

**Pre-work**: Follow `${CLAUDE_PLUGIN_ROOT}/shared/_shared_protocols.md` §1.

## What Cycle Does

Cycle automates the following process (which was proven effective on 2026-03-16 for the Tool Ecosystem Architecture Review):

```
Cycle 1 (Blueprint)  →  DevTeam + Professor  →
Cycle 2 (Blueprint)  →  DevTeam + Professor  →
Cycle 3 (Blueprint)  →  Final DevTeam Audit  →  PDF Output + Learnings
```

Each cycle has a specific role:
- **Cycle 1**: Foundation — raw inventory, gap analysis, initial architecture
- **Cycle 2**: Refinement — incorporate DevTeam fluidity findings + Professor research
- **Cycle 3**: Synthesis — final comprehensive pass with all accumulated knowledge

## When to Trigger

- User says "cycle", "run cycle", "deploy cycle", "use cycle on [topic]"
- User says "iterate on this", "refine this blueprint", "deep blueprint"
- User says "3-pass", "triple-pass", "iterative blueprint"
- User wants a deeply refined plan that goes beyond a single Blueprint pass

## Project Context

Project-agnostic. Paths loaded dynamically from project init skills:
- **UE5/your project**: Source root, docs root, PDF output, project docs detected from your-project-init
- **SaaS projects**: Detected from project package.json and framework configs
- **Any project**: PDF output defaults to project root + `/docs/research/`
- **Learnings File**: `_learnings.md` in this skill's directory
- **Pre-work**: Follow `${CLAUDE_PLUGIN_ROOT}/shared/_shared_protocols.md` §1

## Workflow

### Phase 0: Load Learnings & Parse Request

1. **Check for learnings file** at `_learnings.md` in this skill's directory. If it exists, read it — these are accumulated insights from previous Cycle runs that should inform this run's approach.
2. **Read `.claude/shared/_shared_learnings.md`** — cross-skill learnings applicable to cycle
3. **Read `.claude/shared/bifrost_api_contract.md`** — authoritative API reference for PDF generation
4. **Parse the user's prompt** to extract:
   - **Topic**: What system/feature to blueprint (e.g., "vehicle locomotion", "tool ecosystem")
   - **Scope**: Narrow (single system) or broad (ecosystem-wide)
   - **Existing context**: Any prior research, blueprints, or code already done
5. **Check existing docs**: Search Docs/Design Systems/Research/ and Docs/Design Systems/ for existing professor research and blueprints on this topic. Cycle builds on what exists — never starts from zero.

### Compaction Resilience Protocol

At every phase transition (Cycle 1→2, 2→3), write current state to disk:
1. **State file**: Write accumulated knowledge summary to a temporary file noting: current pass number, key findings so far, devTeam scores, identified gaps
2. **Recovery marker**: Include in conversation: `CYCLE STATE: Pass [N] complete | Topic: [topic] | State file: [path]`
3. **On compaction recovery**: If state is lost, read the state file to restore context before continuing

### Phase 1: Cycle 1 — Blueprint Foundation Pass

**Goal**: Raw inventory and gap analysis. Understand what exists, what's missing, what's broken.

**Blueprint scans:**
- Source code: Grep/Glob for all relevant classes, headers, systems
- Existing docs: Any Professor_, Blueprint_, or project docs section covering this topic
- project docs: Read the relevant chapter(s) from the Complete Game Systems project docs
- Current state: What's working, what's broken, what's a stub

**Output Cycle 1 findings as structured text:**
- Complete inventory (what exists, versions, LOC, status)
- Gap analysis (what's missing, what's misplaced, what needs work)
- Dependency map (what depends on what)
- Initial architecture sketch
- Questions/unknowns for Cycle 2 to resolve

**Then run DevTeam analysis on Cycle 1:**
- Apply 7 Universal Laws to the proposed/existing architecture
- Run Fluidity Checklist on system boundaries
- Flag anti-patterns
- Score coupling/cohesion
- Identify specific gaps for Professor to research

**Then run Professor research on gaps:**
- Target 5-8 web searches specifically addressing DevTeam's identified gaps
- Research best practices from AAA studios and UE5 community
- Collect specific APIs, patterns, performance data
- Cross-reference with existing project docs content

### Phase 2: Cycle 2 — Refinement Pass

**Goal**: Incorporate ALL Cycle 1 + DevTeam + Professor findings into a refined blueprint.

**Blueprint incorporates:**
- All Cycle 1 inventory data
- DevTeam fluidity scores and anti-pattern fixes
- Professor research findings and best practices
- Resolved unknowns from Cycle 1's questions

**Cycle 2 goes deeper:**
- Specific C++ class designs with signatures
- Phased implementation roadmap with dependencies
- Performance budget estimates
- Risk assessment
- Integration points with existing systems

**Then run DevTeam on Cycle 2:**
- Re-score fluidity with the refined architecture
- Check if anti-patterns from Cycle 1 are resolved
- Identify any NEW issues introduced by the refinement
- Validate data contracts between proposed systems

**Then run Professor on remaining gaps:**
- Target 3-5 web searches on specific implementation details
- Focus on edge cases, performance pitfalls, proven patterns
- Gather experimental/cutting-edge approaches

### Phase 3: Cycle 3 — Final Synthesis

**Goal**: Comprehensive, production-ready blueprint incorporating ALL accumulated knowledge.

**Final Blueprint includes:**
1. **Executive Summary** — 3-5 bullet critical decisions
2. **Existing System Audit** — what we have (from Cycle 1)
3. **Architecture Design** — refined class hierarchy (from Cycle 2)
4. **Dependency Matrix** — visual graph with status (from Cycle 1+2)
5. **Phased Implementation Roadmap** — each phase with files, code, deps
6. **Data Architecture** — USTRUCTs, data assets, replication
7. **Performance Budget** — threshold-colored table
8. **Technical Risk Assessment** — probability × impact scoring
9. **DevTeam Fluidity Audit** — 7 Laws scores, anti-patterns, coupling matrix
10. **Professor Insights** — best practices, source-tiered citations
11. **Optimization Recommendations** — from DevTeam analysis
12. **Priority Matrix** — all actions ranked by impact × effort
13. **Cycle Evolution Log** — what improved between cycles (for learnings)

**Final DevTeam audit:**
- Score the complete output
- Compare Cycle 1 → Cycle 2 → Cycle 3 evolution
- Flag any remaining debt

### Phase 4: Generate PDF

Use the Bifrost PDF Generator v3.0:

```python
import sys
sys.path.insert(0, r"~/Desktop\your project721\Tools\BifrostPDF")
from bifrost_pdf import BifrostPDF, BifrostTheme as T

pdf = BifrostPDF(
    title="[Topic] — 3-Cycle Blueprint",
    subtitle="Iterative Refinement: Blueprint + DevTeam + Professor",
    output_path=r"~/Desktop\your project721\Docs\Design Systems\Research\Cycle_[Topic].pdf",
    footer="SWORDER:721 // Cycle Blueprint // [Topic]"
)
```

Save the generator script to `Tools/PDFGenerators/generate_cycle_[topic].py`.

### Phase 5: Record Learnings (AUTO-UPDATE)

**CRITICAL: This phase runs EVERY time Cycle completes. It is what makes Cycle self-improving.**

After generating the PDF, analyze the run and append findings to `_learnings.md`:

```markdown
## Run: [Topic] — [Date]

### What Worked
- [Specific techniques/searches/patterns that produced high-value findings]

### What Was Slow
- [Phases that took too long or produced low-value output]

### Data Sources That Were Most Valuable
- [Which existing docs, project docs, or search queries gave the best info]

### Gaps Discovered
- [Information that was needed but couldn't be found — feed into project docs update candidates]

### Optimization for Next Run
- [Specific improvements: skip X, prioritize Y, search for Z first]

### Cycle Evolution Metrics
- Cycle 1 completeness: [X/10]
- Cycle 2 improvement: [+Y points]
- Cycle 3 final score: [Z/10]
```

**The learnings file is cumulative** — each run appends, never overwrites. Over time, Cycle becomes smarter about:
- Which search queries yield the best results for different topic types
- Which project docs are most relevant per system
- Which DevTeam checks catch the most issues
- Which phases can be compressed for well-covered topics
- Common patterns that apply across multiple systems

## Auto-Update Protocol (Applies to ALL Skills)

Cycle pioneered this pattern, but ALL skills should follow it:

### The Learning Loop
1. **Before execution**: Read `_learnings.md` if it exists
2. **During execution**: Track what works well and what doesn't
3. **After execution**: Append findings to `_learnings.md`
4. **Next invocation**: Learnings inform the approach — skip known dead-ends, prioritize known high-value paths

### Learning File Format
Every skill's `_learnings.md` follows the same schema:
```markdown
# [Skill Name] Learnings

## Run: [Context] — [Date]
### What Worked: [specific techniques]
### What Was Slow: [bottlenecks]
### Optimization: [improvement for next time]
```

### Skills That Should Implement This
- **Professor**: Track which search queries give best results per topic domain
- **Blueprint**: Track which project docs are most relevant per system
- **Analyst**: Track scoring calibration adjustments over time
- **QA Skill**: Track benchmark values that need updating
- **Scanner**: Track PDF locations and content summaries for faster retrieval
- **DevTeam**: Track anti-pattern resolution rates and which Laws catch the most issues
- **Organizer**: Track folder conventions and user preferences
- **Init**: Track which docs are actually referenced vs loaded-but-unused

## Key Principles

- **Each cycle must be BETTER than the last.** If Cycle 2 doesn't improve on Cycle 1, something is wrong.
- **DevTeam is the quality gate.** It identifies what's weak. Professor fills in what's missing.
- **Never start from zero.** Always check existing docs first. Cycle EXTENDS, never replaces.
- **The learnings file is sacred.** It's the memory that makes Cycle get faster and smarter.
- **Show the user Cycle 1 findings** before proceeding to Cycle 2. They may want to steer.
- **Parallel where possible.** DevTeam and Professor run in parallel between cycles (they're independent).
- **C++ first.** All code in the blueprint should be C++ with UPROPERTY/UFUNCTION exposure.
- **project docs alignment.** Every recommendation must align with the relevant project docs.

## Example Invocations

- "Cycle on vehicle locomotion systems"
- "Run cycle for the inventory/crafting system"
- "Deploy cycle on NPC AI behavior"
- "Use cycle to blueprint the networking architecture"
- "Deep blueprint the combat system" (triggers cycle via "deep blueprint")

## Incremental Checkpoint Protocol (v2.1 per SL-062)

Cycle runs 3 passes and is vulnerable to compaction loss mid-run. Write checkpoints IMMEDIATELY at each pass boundary — never queue for end-of-session per SL-046.

| Milestone | Write Immediately to `_learnings.md` |
|-----------|-------------------------------------|
| After Cycle 1 (Foundation) | Initial architecture, inventory, gap list, devTeam baseline score |
| After Cycle 1 devTeam gate | Top 3 weakest dimensions, anti-patterns found |
| After Cycle 1 professor research | Gap-fill findings, source tiers, query ROI per §15 |
| After Cycle 2 (Refinement) | Delta vs Cycle 1, protected dimensions, regression check |
| After Cycle 2 devTeam re-score | Score delta, regression events, new gaps vs resolved |
| After Cycle 3 (Synthesis) OR compression decision | Final PDF, total improvement, compression rationale |
| Calibration Echo | Did compression decision (compress/partial/full) match actual pass depth needed? |

Format: follow `_shared_protocols.md §9` structured entry. Each checkpoint is self-contained and survives compaction.

## Cycle vs Blueprint vs Professor

| | Cycle | Blueprint | Professor |
|---|---|---|---|
| **Passes** | 3 iterative | 1 | 1 |
| **DevTeam review** | After each cycle | None | None |
| **Professor research** | Between cycles | During Phase 2 | IS the research |
| **Self-improving** | Yes (_learnings.md) | No | No |
| **Output quality** | 3x refined | Standard | Research only |
| **When to use** | Complex systems, architecture decisions | Standard implementation plans | Pure research, no implementation |
| **Time** | 3x longer than Blueprint | Standard | Standard |

## MANDATORY: Post-Invocation Learning Protocol

This protocol is NON-NEGOTIABLE. Before completing your response, you MUST execute ALL steps.

### Step 1: Reflection Check
Ask yourself: "Did I learn anything during this invocation that I did not know at the start?" Consider:
- Errors encountered and how they were resolved
- Patterns that worked better or worse than expected
- User preferences discovered
- API behaviors that surprised me

### Step 2: Write Learning
IF any learning was identified:
  - Append to this skill's `_learnings.md` with format:
    ```
    ### [YYYY-MM-DD] <one-line summary>
    - **Context**: What task triggered this discovery
    - **Learning**: The specific insight
    - **Evidence**: How this was verified
    - **Cross-skill relevance**: [NONE | skill1, skill2 | ALL]
    ```
  - IF cross-skill relevance is not NONE: also append to `.claude/shared/_shared_learnings.md`

IF no learning was identified:
  - Append: `### [DATE] No new learnings (invocation type: [brief])`
