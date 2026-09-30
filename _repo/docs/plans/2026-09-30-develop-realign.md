# develop 재정비 — structure, then identity

## Plan

**Why.** `skill/skills/create/references/identity.md` (P1–P13) is now the house standard; it names
`develop/clean-code` and `develop/sql-pro` as the counter-example ("catalog-style reference skills with no stance").
Survey of the 33 develop skills, 2026-09-30:

- 14 are imports (Jeffallan ×11, wondelai ×3), shape unchanged since March.
- Standing Mandates: 5 / 33. `Not for` line: 2 / 33. Named forbidden reflex (P4): ~6 / 33.
- Invocations across 173 local projects (`"skill":"develop:<n>"` in transcripts):
  testing-workflow 26, test-master 22, clean-code 20, scenario-actor 20, domain-driven-design 16,
  scenario-director 16, architecture-designer 12, kotlin-specialist 6, sql-pro 4, transaction-boundary-reviewer 4,
  spring-boot-engineer 3, clean-architecture 3, sre-engineer 2, flaky-test-analyzer 1. **The other 19: 0.**

**What.** Two phases, each its own commit set on a local branch (no push, no version bump).

### Phase 1 — structure (33 → 27)

| Action | Skills | Reason |
|---|---|---|
| Retire to `_repo/deprecated/develop/` | `frontend-developer`, `cli-developer`, `dockerfile-optimizer` | 0 uses; generic how-to Claude does without a skill; no stance to rewrite toward |
| Merge into `architecture-designer` (topology) + `service-boundary-validator` (where to cut) | `microservices-architect` | 0 uses; its two jobs are exactly those two skills |
| Merge into `documentation-strategy` | `code-documenter` | 0 uses both; docstrings/OpenAPI become one purpose of the doc skill |
| Retire | `dev-quality-workflow` | 0 uses; a workflow over the other workflows; CLAUDE.md row repointed to `architecture-workflow` |

No renames: the used skills keep their names (test-master 22 uses — renaming breaks habit for no gain).
Refs repointed everywhere (`grep develop:<retired>` → 0 outside `_repo/`). README/KOR move together.

### Phase 2 — identity rewrite (27 skills, by use, highest first)

Each kept skill gets: Standing Mandates with **one** forbidden reflex (P4) carrying its scar (P10) and a `Goal:` line
(P9); an Output Template that closes on a recountable verdict (P1); a `Not for` + named handoffs (P6);
catalog content cut or moved to `references/` (P12). `scenario-actor` / `scenario-director` already comply — audit only.

Batches: (a) testing — testing-workflow, test-master, TDD, flaky-test-analyzer; (b) code — clean-code,
clean-architecture, kotlin-specialist, spring-boot-engineer; (c) architecture — domain-driven-design,
architecture-designer, service-boundary-validator, event-storming, architecture-workflow; (d) DB — sql-pro,
transaction-boundary-reviewer, database-optimizer, connection-pool-tuner, database-workflow; (e) ops — sre-engineer,
incident-response-playbook, chaos-engineer, circuit-breaker-tuner, performance-profiling-optimization,
operations-workflow; (f) docs — documentation-strategy.

## Done criteria

- [ ] Phase 1: 27 skill dirs; `grep -r "develop:(frontend-developer|cli-developer|dockerfile-optimizer|microservices-architect|code-documenter|dev-quality-workflow)"` outside `_repo/` → 0.
- [ ] `_repo/scripts/validate_plugins.py` → `[develop]` OK after each phase.
- [ ] Phase 2, every kept skill: Standing Mandates with exactly one NEVER/Do NOT reflex + reason + `Goal:`; `Not for`
      line; description ≤ 250 chars starting `Use when`; body not longer than today.
- [ ] Each batch passes `skill:quality-assurance` (run in a separate context — P3), verdicts quoted in the commit.
- [ ] README.md + KOR.md list the same 27 skills.
- [ ] Local branch only; no push, no version bump.

## Critique

- **0 uses ≠ useless** (memory: no-references-is-not-unused). The 0-use set includes skills edited today
  (incident-response-playbook, performance-profiling-optimization, event-storming). Only retire the three with no stance
  *and* 0 uses; the rest are rewritten, not cut.
- **Merges lose content.** Anything from the merged skill that the target lacks goes to the target's `references/`,
  not dropped.
- **Phase 2 is large** (~27 rewrites). Batched so each batch is reviewable alone; user can stop after any batch.
- **Trigger overlap** with `superpowers:test-driven-development` and `write:writing-skills`-style collisions is out of
  scope; noted if trigger-validator flags it.

## Revision 2026-09-30 (user): rewrite all, in parallel

User: "skill: 들을 바탕으로 전체적으로 재작성하자 — 1. 최소 동작 보정 2. persona 강화 3. mcp나 다른 tool 필요하다면 확장 — 병렬로".
Phase 2 runs over all 33 skills (six parallel batches, method = `skill:create` steps 2–7 applied to an existing skill).
Phase 1 (retire/merge) is not approved yet and is not executed; the six candidates are rewritten like the rest.
Tools/MCP are added to `compatibility` only where a Process step uses them (P12).
Per-skill `quality-assurance` (6 agents each) is replaced by one independent identity reviewer per batch (P3), for cost.
