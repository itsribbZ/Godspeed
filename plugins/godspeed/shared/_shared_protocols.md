# Holy Tool Shared Protocols v2.1
<!-- v2.1 (2026-04-10): §1 enhanced with grep-first load mandate. Added §12 Prompt Cache Discipline, §13 Failure Recovery Primitives, §14 Session State Persistence, §15 Query ROI Tracking Schema. Additive-only per SL-035. See SL-062 for audit rationale. -->
<!-- Referenced by: holy-trinity, devTeam, profTeam, godspeed, cycle, professor, blueprint -->
<!-- Single source of truth. Do NOT duplicate these protocols inline in SKILL.md files. -->

## 1. Pre-Work Loading

Before beginning any skill invocation:
1. Read `~/.claude/shared/_shared_learnings.md` — **grep-first, never bulk-read** (v2.1). Use: `grep -B1 -A10 "applies_to.*[your-skill]\|applies_to.*ALL" _shared_learnings.md`. Loads only matching entries (~40 lines avg) instead of the full 336-line file. Apply HIGH/MEDIUM matches only. Bulk-read is a Law 5 Liability violation per SL-062.
2. If UE5/your project project: also read `~/.claude/shared/_shared_learnings_ue5.md`
3. Apply all HIGH/MEDIUM learnings
4. If generating PDFs: read `~/.claude/shared/bifrost_api_contract.md`
5. For data contracts: reference `~/.claude/shared/skill_dependency_graph.md`

## 2. Source Tier System

| Tier | Source Type | Standalone? |
|------|-----------|-------------|
| T1 | Official docs, API reference, framework maintainers | With corroboration |
| T2 | GDC talks, AAA postmortems, named practitioners | With corroboration |
| T3 | Peer-reviewed academic (ACM, IEEE) | With corroboration |
| T4 | Engine/framework source analysis | Needs T1-T3 backup |
| T5 | Community tutorials, forums | NEVER standalone |

**Verified Data Floor:**
- **VERIFIED**: ≥2 independent T1-T3 sources → implementation-ready
- **PROBABLE**: 1 T1-T3 source → proceeds with `[PROBABLE]` tag
- **UNVERIFIED**: T4/T5 only → BLOCKED from implementation
- **Engine-Version Exception**: T4 + T2 = VERIFIED when T1 docs lag. Tag: `[VERIFIED-ENGINE-SOURCE]`

## 3. Parallel Execution

ALL agents MUST deploy in a SINGLE response message. Never sequential unless output dependency exists.

```
❌ Deploy A → wait → Deploy B → wait → Deploy C
✓ Single message: [A] + [B] + [C] → all fire simultaneously
```

File reads: load ALL priority files in ONE parallel batch.

## 4. Post-Invocation Learning (MANDATORY)

After EVERY invocation, execute these steps:

**Reflect**: What worked? Calibration accuracy? Anti-patterns found? Cross-skill relevance?

**Write**:
- Checkpoints already written → append consolidation entry linking to them
- No checkpoints → full structured entry to skill's `_learnings.md`
- Cross-skill relevance → also append to `_shared_learnings.md`
- Nothing learned → `### [DATE] No new learnings (type: [brief])`

**Update Shared**:
- BifrostPDF issue → update `bifrost_api_contract.md`
- New pattern → append to `_shared_learnings.md` (grep max SL-ID first per SL-043)
- Dependency change → update `skill_dependency_graph.md`

## 5. Incremental Checkpoints (Compaction-Resistant)

Write learnings DURING execution, not just at the end. Context compaction kills end-of-session writes.

| Milestone | Write Immediately |
|-----------|------------------|
| After scoring/diagnosis | Calibration, gaps, anti-patterns |
| After each agent returns | ROI, key finding, source quality |
| After cross-reference | Validation results, compression decision |
| After regression fires | Regression details (CRITICAL — never lose) |
| Shared learnings (SL-NNN) | IMMEDIATELY — never queue for later |

Format: `### [DATE] [Target] — Phase [N] Checkpoint` + 1-3 bullets.

## 6. Session Safety

**SL-ID Allocation**: grep max existing ID, use N+1. Never hardcode.
```bash
grep -oP 'SL-\K\d+' ~/.claude/shared/_shared_learnings.md | sort -n | tail -1
```

**Checkpoint Dirs**: `[skill]_[topic]_[YYYYMMDD_HHMMSS]_[4hex]/` — prevents collision.

**Append Safety**: Self-contained blocks only. No read-modify-write on `_learnings.md`.

## 7. Learning Pipeline Health Check

Run during init or periodically:
1. Count `_learnings.md` entries per skill — flag <5 entries after 10+ invocations as "pipeline broken"
2. Verify no duplicate SL-IDs in `_shared_learnings.md`
3. Check staleness: any `_learnings.md` >30 days without update → flag
4. Verify skills reference this file (not inline duplicates)

Entry counts should grow proportionally to invocations. A skill with 20+ invocations and <5 entries = checkpoint protocol not firing.

## 8. Additive Upgrade Discipline

When modifying skill files (SKILL.md, _learnings.md, shared infra):
- ZERO REMOVALS without user approval
- Changes are additive layers on top of existing content
- Existing content preserved unless factually incorrect
- Flag removals: `[FLAG: REMOVAL NEEDED — reason]` — blocked pending user decision

## 9. Structured Learning Entry Format (v2.0)

All learning entries across ALL skills MUST use this structured format for machine-readable parsing:

```markdown
### [ENTRY_TYPE]: [Target/Topic] — [YYYY-MM-DD]
<!-- meta: { "run_id": "[skill]_[topic]_[date]", "domain": "[domain]", "confidence": "[HIGH/MEDIUM/LOW]", "confirmed_count": [N], "roi_score": [1-5], "staleness_check": "[YYYY-MM-DD]" } -->

**Finding**: [One-sentence summary of the learning]
**Evidence**: [What proved it — source tier, run data, or empirical observation]
**Applies to**: [skill1, skill2, ALL]
**Action**: [What to DO differently based on this learning]
```

Entry types: `Score`, `Calibration Echo`, `Anti-Pattern`, `Recovery Event`, `Query ROI`, `Aggregate`, `Prediction Accuracy`, `Escalation`, `Checkpoint`, `Run`

The `<!-- meta: {...} -->` comment is invisible in markdown rendering but parseable by any skill that reads the file. This enables:
- Automated ROI computation across all skills
- Staleness detection (entries not confirmed in X days)
- Confidence-weighted decision making
- Cross-skill pattern matching by domain

**Backward compatibility**: Existing free-form entries remain valid. New entries use structured format. Over time, the ratio shifts toward structured.

## 10. Cross-Skill Auto-Promotion

When a learning is independently discovered or confirmed by 2+ different skills, it should be promoted to `_shared_learnings.md`:

### Auto-Promotion Protocol
1. **After writing a learning entry**, scan `_shared_learnings.md` for similar findings
2. **If match found**: Increment `confirmed_count` on the shared entry, add confirming skill to `Confirmed by` field
3. **If no match but finding is cross-applicable**: Check if the same pattern appears in another skill's `_learnings.md`
   - If yes → promote to shared with `confirmed_count: 2`
   - If no → leave in skill-local learnings (not yet cross-validated)
4. **Promotion threshold**: A finding in 2+ skill-local learnings OR confirmed by user → auto-promote
5. **Format**: Follow §9 structured format + standard SL-ID allocation (§6)

### What qualifies for promotion:
- Pattern works across domains (not domain-specific)
- Tool/API behavior that affects multiple skills
- Operational insight about agent deployment, context management, or research efficiency
- User preference or feedback applicable to all skills

### What stays skill-local:
- Domain-specific calibration data (e.g., UE5 API behavior → stays in ue5 learnings)
- Single-run observations not yet confirmed
- Topic-type-specific agent configs (stays in profTeam)

## 11. Learning Staleness Detection

Learnings decay. A finding from 90+ days ago may be outdated. Skills must actively manage staleness.

### Staleness Protocol
1. **On every skill invocation**, check `staleness_check` dates in loaded learnings
2. **Flag stale entries** (not confirmed in 60+ days):
   - `STALE-WARNING`: 60-90 days since last confirmation → use with caution, verify before applying
   - `STALE-CRITICAL`: 90+ days → do NOT apply automatically. Verify first, then either:
     - Re-confirm (update `staleness_check` and `confirmed_count`)
     - Archive (move to bottom of file under `## Archived Learnings`)
3. **Auto-refresh**: When a stale learning is re-confirmed during a run, update its `staleness_check` to today and increment `confirmed_count`
4. **Health metric**: `freshness_ratio = entries_confirmed_in_60d / total_entries`. Report if < 0.5.

### Staleness does NOT apply to:
- User directives (SL-008, SL-009, SL-035) — these are permanent unless user changes them
- API contracts (SL-001, SL-002, SL-003) — verify against source, not by time
- Architectural facts (SL-033) — verify against tool behavior, not by time

## 12. Prompt Cache Discipline (v2.1)

Claude's prompt cache gives ~10× discount on cache hits. Order every agent prompt to maximize reuse. Source: Anthropic Prompt Caching docs (T1).

### Cache-First Ordering
Build agent prompts top → bottom:
1. **Invariant block** (cacheable): tool list, 7 Laws table, source tiers, PROVEN QUERIES, SOP
2. **Semi-stable block** (cacheable per session): domain context, skill contracts, filtered shared learnings
3. **Volatile block** (uncacheable): topic, per-run gaps, current payload, per-target details

### Rule
Never interleave volatile data into invariant blocks. Once the cache boundary breaks, every subsequent token pays full rate.

### Applies to
profTeam (Phase 1 agent dispatch), devTeam (scoring prompt construction), holy-trinity (all phase prompts), cycle (per-pass), professor (research prompt), godspeed (agent deployment).

**Expected savings**: 50-80% per-invocation cost on repeated-prefix workloads (per T1 Anthropic Prompt Caching + T3 arxiv 2603.18897 Act While Thinking).

## 13. Failure Recovery Primitives (v2.1)

Consolidates failure recovery catalogs previously duplicated across devTeam, profTeam, trinity, debug. Reference this section — do not re-narrate inline per SL-062.

| Mode | Trigger | Recovery |
|------|---------|----------|
| Compaction mid-run | Context lost mid-session | Read `manifest.json` → reconstruct task list → resume from last checkpoint |
| Agent crash | Empty return or timeout | Mark agent ROI=0, redeploy with tighter scope OR skip if optional |
| Tool error | Non-zero exit from Edit/Bash/Write | Log, downgrade to L2 (instrument), never retry blindly |
| Partial result | Agent incomplete output | Salvage findings, flag gaps, proceed with partial data + note |
| File clobber (SL-056/SL-061) | IDE overwrites external edit | Grep to confirm, re-apply edit, rebuild before IDE saves again |
| Stale state | Checkpoint file >24h old | Archive and start fresh — do not resume from stale state |

### Recovery Marker
Every resumable skill writes at session start:
`[SKILL] SESSION: [YYYYMMDD_HHMMSS] | STATE: [path_to_manifest.json]`

On recovery: grep for the marker, read manifest, resume from first pending task in priority order.

## 14. Session State Persistence (v2.1)

Consolidates checkpoint directory patterns from profTeam, godspeed, debug, cycle. Canonical pattern for ALL checkpointing skills.

### Directory Pattern
`~/.claude/skills/[skill]/.state/[skill]_[topic]_[YYYYMMDD_HHMMSS]_[4hex]/`

The 4-char hex suffix prevents collision between concurrent runs on the same topic.

### Manifest Schema
`manifest.json` at directory root:
```json
{
  "session_date": "YYYY-MM-DD",
  "skill": "[skill]",
  "topic": "[topic]",
  "domain": "[detected]",
  "tasks": [{"id": 1, "priority": "P0", "status": "done|pending|blocked|deferred", "description": "..."}],
  "checkpoints": [{"phase": "N", "timestamp": "...", "file": "phase_N.md"}],
  "agents": [{"id": "A", "roi": 4, "mvp": true, "file": "agent_A.md"}],
  "escalations": []
}
```

### Cleanup
- Archive state dir after session reconciliation
- Orphaned state >24h old: safe to delete on next invocation
- NEVER delete mid-session — compaction recovery depends on it

## 15. Query ROI Tracking Schema (v2.1)

Closes the SL-048 Query ROI feedback loop. Turns theoretical infrastructure into measured data that compounds expertise over time.

### Per-Query Tag (in agent checkpoint JSON)
```json
{
  "query": "exact query string",
  "roi": 5,
  "tier": 1,
  "useful": true,
  "hits_used": 3,
  "hits_discarded": 1
}
```

### ROI Scale
- **5**: Found root cause or verified pattern
- **4**: Surfaced useful detail or context
- **3**: Partial signal, required follow-up
- **2**: Low value, confirmed known data
- **1**: Zero signal
- **0**: Wasted tokens (noise/spam/broken pages)

### Aggregation (at end of run)
Append to skill's `_learnings.md`:
```markdown
### Query ROI: [Topic Type] — [Date]
HIGH-ROI (≥4): [list of queries]
LOW-ROI (≤2): [list of queries — AVOID next run]
```

### Proven Query Injection (before next run)
Grep skill's `_learnings.md` for prior `Query ROI: [same topic-type]` entries. Inject top-3 HIGH-ROI queries as `PROVEN QUERIES` block into agent prompts. Flag LOW-ROI patterns as `AVOID`.

### Applies to
profTeam (Phase 1 + Phase 6), professor (research block), debug (Phase 2 context gather), cycle (per-pass research).

**Expected impact**: After 10+ runs on the same topic type, search cost drops ~30-40% and quality climbs (per SL-048 theoretical model + T3 arxiv 2510.16079 EvolveR Self-Evolving Agents).
