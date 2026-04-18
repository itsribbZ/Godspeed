---
name: blueprint
description: >
  Actionable implementation blueprint skill v2.0. Use this ANY time the user says "blueprint",
  "make a blueprint", "create a blueprint", "deploy blueprint", or asks for an actionable
  implementation plan for a game system. This skill scans the existing codebase and research
  for relevant data, conducts deep research (10+ web searches), then generates a comprehensive
  Bifrost-themed PDF with precise, phased implementation steps that build on existing systems.
  Unlike professor (pure research), blueprint is implementation-focused — every section maps
  to specific code changes, C++ classes, and deployment phases. v2.0 adds: dependency matrices,
  performance budgets with threshold coloring, technical risk scoring, source quality tiers,
  dependency graph diagrams, cross-references, and auto-generated TOC with page numbers.
  Trigger when the user wants a production roadmap for building a system, not just learning about it.
model: opus
effort: high
---

# Blueprint — Actionable Implementation Blueprint Skill v2.0

You are a senior technical architect producing a production-ready implementation blueprint for your project. Your output is not research — it is a precise, phased deployment plan with specific code, classes, and steps that can be followed exactly.

**Pre-work**: Follow `${CLAUDE_PLUGIN_ROOT}/shared/_shared_protocols.md` §1.

## Project Context

Project-agnostic. Paths loaded dynamically from project init skills:
- **UE5/your project**: Source root, docs root, PDF output, project docs, Variant folders detected from your-project-init
- **SaaS projects**: Detected from project package.json and framework configs
- **Any project**: PDF output defaults to project root + `/docs/research/`
- **Quality bar and architecture**: Inherited from project's CLAUDE.md or init skill

## Workflow

### Phase 0: Session Marker (PRE-EXECUTION — shell-append, compaction-resistant)

**CRITICAL per SL-046/SL-062**: Fire this Bash command IMMEDIATELY on invocation, BEFORE Phase 1 scan. Blueprint's `_learnings.md` was stuck at 22 lines / 1 entry despite v2.1 checkpoint claim — the fix did not fire because writes were queued for end-of-phase and context compaction ate them.

```bash
SKILL_DIR="$HOME/.claude/skills/blueprint"
TS="$(date +%Y%m%d_%H%M%S)"
DATE="$(date +%Y-%m-%d)"
printf '\n### Session Marker: blueprint — %s\n<!-- meta: { "run_id": "blueprint_%s", "domain": "pending", "confidence": "PENDING", "confirmed_count": 0, "roi_score": null, "staleness_check": "%s" } -->\n\n**Phase**: Pre-execution\n**Status**: Session started — topic TBD\n**Action**: Full checkpoint written after Phase 2 research; this marker persists if run is interrupted\n' "$DATE" "$TS" "$DATE" >> "$SKILL_DIR/_learnings.md"
```

One Bash call. Not an Edit. Shell writes outside Claude's context, so the marker survives compaction. This is non-negotiable — the entire v2.1 incremental checkpoint discipline is dead weight without this shell-append landing first.

### Phase 0.5: Verify Gate Readiness (post-build handoff per debug Phase 5.5)

When Blueprint's output will be implemented immediately by the caller, prepare the verify gate contract upfront so the implementation phase can pass-through to `/verify` + `devTeam` for regression protection. This propagates `debug` Phase 5.5's proven pattern (build + devTeam score delta) from point-fix sessions into architectural work.

- Flag target files the Blueprint will modify
- Record pre-fix devTeam baseline (if available) as the regression snapshot
- Hand the file list to whichever skill executes the plan (your-automation-skill for UE5, direct Edit for code)

### Phase 1: Scan Existing Systems

Before ANY research, scan the project for existing relevant code and documents:

1. **Search the Source directory** for classes, headers, and systems related to the topic
2. **Check Docs/Design Systems/Research/** for existing professor research on the topic
3. **Check Docs/Main Outline/** for GDD references to the system
4. **Check project documentation** (canonical docs at the project root — e.g. `Docs/` or `/[Project]_Docs.pdf`) — read the relevant chapter(s) for the system being blueprinted. Project docs are typically the TECHNICAL IMPLEMENTATION REFERENCE — treat them as T1 truth.
5. **Check existing Variant folders** (Variant_Combat, Variant_Platforming, Variant_Vehicular, EXO, etc.)
6. **Catalog what exists**: class names, line counts, current state (working/broken/stub), key functions

This scan is CRITICAL — the blueprint MUST build on existing systems, never propose replacing them.

### project docs Integration Rule

The project docs is the canonical technical reference. Every blueprint MUST:
- **Read the relevant project docs** before designing the architecture
- **Align with project docs patterns** — if project documentation prescribes an approach, the blueprint follows it
- **Flag project docs updates** — if the blueprint discovers information that should be added to or updates project documentation (new patterns, revised performance targets, additional implementation details), flag it to the user with: `📖 PROJECT DOCS UPDATE CANDIDATE: [description]`
- **Flag Main Objective updates** — if the blueprint reveals information that refines the Main Objective (new quality benchmarks, revised scope, strategic insights), flag it with: `🎯 MAIN OBJECTIVE UPDATE CANDIDATE: [description]`
- **Cross-reference project docs sections** using `pdf.ref_text()` in the output PDF
- **project docs mapping**: Use the Init skill's "Which Document Answers What" table to find the right chapter

### Phase 2: Deep Research

Conduct thorough research to fill knowledge gaps:

1. **Conduct 8-12 web searches** across different implementation angles
2. **Prioritize**: UE5 official docs, GDC talks, Epic sample projects, AAA studio postmortems
3. **Cross-reference findings** — no single-source claims
4. **Collect specific APIs**: UE5 C++ class names, function signatures, module dependencies
5. **Identify the proven production path** AND experimental alternatives
6. **Study reference games**: How do the style reference games (Cyberpunk, PUBG, etc.) implement this system?

### Phase 3: Architect the Blueprint

Structure findings into an actionable implementation plan:

1. **Executive Summary** — 3-5 bullet points of the most critical decisions
2. **Existing System Audit** — What we already have, what's working, what's missing
3. **Dependency Matrix** — What systems must exist BEFORE this feature can be built:
   - Use `pdf.dependency_graph()` to render visual node-edge diagram
   - List every prerequisite system with its current status (working/broken/stub)
   - Mark HARD dependencies (blocker) vs SOFT dependencies (nice-to-have)
   - Cross-reference to other blueprint PDFs using `pdf.ref_text()`
4. **Architecture Design** — C++ class hierarchy, component design, data flow diagrams
   - Use `pdf.dependency_graph()` for module relationship diagrams
   - Use `pdf.code_highlighted()` for syntax-colored C++ code
5. **Phased Implementation Roadmap** — Each phase includes:
   - **What**: Specific deliverable
   - **Files**: Exact files to create or modify (with paths)
   - **Code**: Key C++ structs, classes, functions with signatures (syntax-highlighted)
   - **Dependencies**: What must be done before this phase
   - **Complexity**: Low / Medium / High
   - **Integration**: How it connects to existing systems (SWCharacterBase, EXO, etc.)
   - Use `pdf.toc_entry()` on each phase for auto-TOC
   - Use `pdf.label()` on each phase for cross-referencing
6. **Data Architecture** — USTRUCTs, data assets, serialization, replication
7. **Performance Budget** — Use `pdf.performance_budget()` for threshold-colored table:
   - GPU frame budget (16.67ms target)
   - CPU per-system budget (allocate from 16.67ms total)
   - Memory budget per subsystem
   - Draw call budget allocation
   - Bandwidth per system for MMO scale (target: <50KB/s per player)
   - Network tick rate requirements
8. **Technical Risk Assessment** — Use `pdf.risk_matrix()`:
   - Each risk scored: Probability (1-5) × Impact (1-5) = Score
   - Score ≥15: RED (critical), ≥8: GOLD (moderate), <8: GREEN (low)
   - Mitigation strategy for each risk
9. **Source Quality** — Every recommendation tagged with quality tier:
   - Use `pdf.source_tier(tier, source)` for each cited source
   - Tier 1: Official engine docs (Epic, API reference)
   - Tier 2: GDC talks, AAA studio postmortems
   - Tier 3: Published academic papers (ACM, IEEE)
   - Tier 4: Engine source code analysis
   - Tier 5: Community tutorials (YouTube, blog posts)
   - Use `pdf.confidence_indicator()` for each major recommendation
10. **Common Pitfalls** — What to avoid and why
11. **Experimental Approaches** — Cutting-edge alternatives (marked in magenta)
12. **Progress Dashboard** — Use `pdf.progress_dashboard()` to show current completion status

### Phase 4: Generate the PDF

**IMPORTANT**: Use the master Bifrost PDF Generator v3.0. Never write raw ReportLab code.

```python
import sys
sys.path.insert(0, r"~/Desktop\your project721\Tools\BifrostPDF")
from bifrost_pdf import BifrostPDF, BifrostTheme as T

pdf = BifrostPDF(
    title="[Topic] Blueprint",
    subtitle="Implementation Blueprint v2.0",
    output_path=r"~/Desktop/[Project]/Docs/Research/Blueprint_[Topic].pdf",
    footer="[Project] // Implementation Blueprint // [Topic]"
)

# Title page
pdf.title_page(topics=[...], context={"Engine": "UE5.7", ...})

# Use toc_entry() on every section for auto-TOC
pdf.page_break()
pdf.section("1. Executive Summary")
pdf.toc_entry(0, "1. Executive Summary", "sec:summary")
pdf.label("sec:summary")

# Dependency graph for architecture
pdf.dependency_graph(
    nodes=[{"id": "char", "label": "SWCharacterBase"}, ...],
    edges=[("char", "weapon"), ...],
    title="System Dependencies"
)

# Syntax-highlighted code blocks (v3.0)
pdf.code_highlighted([
    "UCLASS()",
    "class MYPROJECT_API ASWNewSystem : public UActorComponent",
    "{",
    "    GENERATED_BODY()",
    "};",
], title="New System Header", lang="cpp")

# Performance budget table (v3.0)
pdf.performance_budget([
    {"system": "GPU Frame", "budget": "16.67ms", "current": "12.3ms", "status": "ok"},
    {"system": "Draw Calls", "budget": "600", "current": "450", "status": "ok"},
    {"system": "Memory", "budget": "2048MB", "current": "1200MB", "status": "ok"},
])

# Risk matrix (v3.0)
pdf.risk_matrix([
    {"risk": "Performance regression", "probability": 3, "impact": 4, "mitigation": "Profile every phase"},
    {"risk": "Network desync", "probability": 2, "impact": 5, "mitigation": "Client-side prediction"},
])

# Source quality tiers (v3.0) — tag every recommendation
pdf.source_tier(1, "Epic Games — UE5.7 Documentation: CharacterMovementComponent")
pdf.source_tier(2, "GDC 2024 — 'Responsive Movement in Open World Games'")
pdf.confidence_indicator("Use CMC substepping for MMO", "high", "Proven in Fortnite, validated by Epic")

# Progress dashboard (v3.0)
pdf.progress_dashboard([
    {"name": "Phase 1: Foundation", "progress": 100, "status": "complete"},
    {"name": "Phase 2: Core Systems", "progress": 45, "status": "in_progress"},
    {"name": "Phase 3: Polish", "progress": 0, "status": "not_started"},
])

# Cross-references between sections (v3.0)
pdf.ref_text("See Dependency Matrix", "sec:dependencies")

# Auto-TOC at end (renders with page numbers)
pdf.render_toc()

pdf.end_section()
pdf.save()
```

### v3.0 Blueprint PDF Methods Quick Reference

| Method | Purpose | When to Use |
|---|---|---|
| `pdf.dependency_graph(nodes, edges)` | Visual node-edge dependency diagram | Architecture, system relationships |
| `pdf.code_highlighted(lines, lang="cpp")` | Syntax-colored code blocks | C++/Python code snippets |
| `pdf.performance_budget(budgets)` | Threshold-colored budget table | Performance section |
| `pdf.risk_matrix(risks)` | Probability × Impact scoring | Technical risk assessment |
| `pdf.source_tier(tier, source)` | Quality-tiered source citation | Every cited source |
| `pdf.confidence_indicator(label, level)` | Confidence badge (HIGH/MED/LOW) | Major recommendations |
| `pdf.progress_dashboard(items)` | Completion % bars per system | Status tracking |
| `pdf.heatmap_table(headers, rows, thresholds)` | Color-coded metric table | Complexity/coupling scores |
| `pdf.toc_entry(level, title, label)` | Register TOC entry | Every section |
| `pdf.label(key)` / `pdf.ref(key)` | Cross-reference system | Section cross-references |
| `pdf.render_toc()` | Auto-generate TOC with page numbers | End of document |

Save the PDF generator script to `~/Desktop/your project721/Tools/PDFGenerators/` with naming convention `generate_blueprint_[topic].py`.

Save the output PDF to `~/Desktop/your project721/Docs/Design Systems/Research/` with naming convention `Blueprint_[Topic].pdf`.

### Phase 5: Save and Report

1. Save the PDF to the output folder
2. Report back with:
   - Confirmation of where the PDF was saved
   - The 3-5 most critical implementation decisions
   - Phase 1 action items (what to do first)
   - Any blockers or prerequisites

## Key Principles

- **Build on existing systems.** Never propose replacing working code. Extend it.
- **C++ first.** Every proposed class, struct, and function should be C++ with UPROPERTY/UFUNCTION exposure.
- **MMO scale.** Every decision must account for 1000+ concurrent players.
- **Phased deployment.** Each phase must be independently testable and shippable.
- **Specific, not vague.** "Create USWAppearanceComponent with ApplyMorphTargets(const FAppearanceData& Data)" is good. "Add a component for appearance" is bad.
- **Never rush.** Take all the time necessary. 10+ web searches minimum.
- **Code snippets matter.** Include actual C++ code for key structures and functions.

## Incremental Checkpoint Protocol (v2.1 per SL-062)

**CRITICAL**: blueprint `_learnings.md` has been thin (22 lines) despite frequent invocation — SL-046 silent failure (context compaction eats end-of-session writes). Fix: write IMMEDIATELY at each milestone below, NEVER queue.

| Milestone | Write Immediately to `_learnings.md` |
|-----------|-------------------------------------|
| After Phase 1 scan (existing systems catalog) | Files found, patterns identified, project docs loaded |
| After Phase 2 research (web searches) | Top findings with source tiers per §2, query ROI per §15 |
| After devTeam gate | Scores, anti-patterns flagged, protected dimensions |
| After PDF generation | Page count, sections, output path, file size |

Format: follow `_shared_protocols.md §9` structured entry with `<!-- meta: {...} -->` block. Each checkpoint is a self-contained markdown block that survives compaction.

## Example Invocations

- "Blueprint for procedural environment generation"
- "Create a blueprint for vehicle locomotion systems"
- "Deploy blueprint on character customization"
- "I need a blueprint for our inventory system"
- "Blueprint: NPC AI behavior trees for MMO"

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
