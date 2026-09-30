---
name: database-workflow
description: >-
  Use when DB performance is degraded and the slow layer is unknown — query, server, pool, or transaction. Triggers: "database workflow", "DB 성능 전체", "DB 전체 점검", "database performance investigation".
type: workflow
theme: engineering
effort: high
scenarios:
  - "Run the database workflow on our slow production DB"
  - "Database performance investigation — find which layer is slow"
  - "Check queries, pool, and transactions for our new DB-heavy feature"
  - "DB 성능 문제 처음부터 끝까지 점검해줘"
  - "프로덕션 DB가 너무 느려 — 어느 레이어 문제인지 봐줘"
estimated_time: "not estimated — depends on the evidence the user supplies"
compatibility:
  optional:
    - sequential-thinking
  remote_mcp_note: >-
    sequential-thinking은 사용자가 준 수치로 느린 레이어를 먼저 특정한 뒤 단계를 진행하도록 순서를 강제합니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER run all four steps in order as a checklist, or start at step 1, before locating the slow layer from the user's own numbers when the job is a slowdown. A full pass with no entry point tunes a healthy layer — an index on a query that was never slow, while the pool sat exhausted.
- NEVER run DDL, or any write, against a real database without the user's explicit go — an index build or parameter change in steps 1–3 is such an act. The sub-skills prepare statements; the user runs them. `EXPLAIN ANALYZE` on DML executes the write.
- NEVER skip a step on your own reading. A skip rests on the user's quoted evidence (EXPLAIN, pool metrics) or is marked `[확인 필요: ○○]` and asked once. Only the step skill's output judges its layer.
- Goal: every step is run or skipped with the user's evidence quoted. Stop when the four are accounted for, or a step ends in `[확인 필요]` the user has not answered.

# Database Workflow

Routes a database slowdown to the layer the user's numbers point at: query → server → pool → transaction.

Also runs as a design / audit pass — a new DB-heavy feature, or onboarding to an existing DB layer — with no slowdown to locate (see Design / audit entry).

**Not for** a single query rewrite (develop:sql-pro), pool sizing alone (develop:connection-pool-tuner), or a transaction review alone (develop:transaction-boundary-reviewer).

## Process

1. **Query quality — `develop:sql-pro`.** Enter with the slow query, schema, engine + version, and the user's `EXPLAIN (ANALYZE, BUFFERS)`. Skip only if that EXPLAIN is quoted and shows no sequential scan on a large table.
2. **Server level — `develop:database-optimizer`.** Enter with the step-1 plan and the deployment type (self-managed vs RDS/Cloud SQL). Skip only if the user's metrics are quoted and show a healthy baseline.
3. **Connection layer — `develop:connection-pool-tuner`.** Enter with DB core count, disk type, pool settings, and the symptom. Skip only if pool metrics are quoted with no timeouts and no sustained pending at peak.
4. **Transaction safety — `develop:transaction-boundary-reviewer`.** Enter with the service and repository code and the inconsistency symptom. Skip only if the service is read-only or the quoted code shows single-table writes with no external I/O inside transactions.

**Design / audit entry.** With no slowdown and no EXPLAIN or pool numbers yet, run all four steps from code: schema and queries-to-be (step 1), deployment and config (step 2), pool config (step 3), transaction boundaries (step 4). Numbers not yet measured (row counts, EXPLAIN, pool metrics, peak load) are marked `[확인 필요: ○○]`, never estimated. Output is findings; the user runs any DDL or config change.

Before step 1, read what the user pasted and pick the entry step from it; ask in one line only when no layer is indicated and the job is a slowdown, not design / audit. Direct entry stays: "커넥션 풀부터" → step 3; "트랜잭션 경계만" → step 4. Use `sequential-thinking`, if available, to hold that order. Each step's own skill defines its input and output; do not restate them here.

## Output Template

```
| Step | Skill | Run / Skipped | Evidence (quote) |
| 1 | develop:sql-pro | … | … |
| 2 | develop:database-optimizer | … | … |
| 3 | develop:connection-pool-tuner | … | … |
| 4 | develop:transaction-boundary-reviewer | … | … |
Slow layer: <layer — the quoted number that shows it> or [확인 필요: ○○]
Verdict: <n> of 4 steps run, <n> skipped with quoted evidence, <n> marked [확인 필요]
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Picks the entry step from your quoted numbers and hands each step to its skill | Provide EXPLAIN output, pool metrics, and code |
| Records run / skipped with the quote that justifies each | Run index DDL, `ALTER SYSTEM`, and pool changes yourself |
| Stops at `[확인 필요]` instead of skipping | Decide which findings to apply and in what order |

## Related Skills

- `develop:sql-pro`, `develop:database-optimizer`, `develop:connection-pool-tuner`, `develop:transaction-boundary-reviewer` — the four steps
- `develop:architecture-designer` — when the schema itself needs redesign
- `develop:spring-boot-engineer` — JPA and `@Transactional` implementation
- `develop:sre-engineer` — monitoring and alerting on DB golden signals afterward
