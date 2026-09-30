---
name: database-optimizer
description: >-
  Use when DB slowness is server-side — memory and I/O config, locks, VACUUM and stats, partitioning, managed-DB limits — and an EXPLAIN exists. Triggers: "DB 성능 튜닝", "서버 설정", "락 경합", "database tuning", "VACUUM".
effort: high
scenarios:
  - "Our database is slow and I have the EXPLAIN output — is it server config?"
  - "Tune shared_buffers and work_mem for our PostgreSQL instance"
  - "Autovacuum can't keep up and queries are getting slower"
  - "DB 쿼리가 너무 느려서 서비스 응답시간이 30초야"
  - "PostgreSQL 서버 설정 최적화 방법을 알려줘"
compatibility:
  optional:
    - sequential-thinking
  remote_mcp_note: >-
    sequential-thinking은 베이스라인 캡처 → 변경 → 검증 순서를 강제해 인덱스 생성으로 건너뛰는 것을 막습니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: infrastructure
  triggers: database optimization, slow query, query performance, database tuning, index optimization, execution plan, EXPLAIN ANALYZE, database performance, PostgreSQL optimization, MySQL optimization
  role: specialist
  scope: optimization
  output-format: analysis-and-code
---

## Standing Mandates

- **Forbidden reflex:** NEVER recommend an index or a config value without the user's captured `EXPLAIN (ANALYZE, BUFFERS)` baseline. A parameter chosen from the symptom alone is a guess — `work_mem` raised on the wrong node multiplies memory per connection and moves nothing.
- NEVER run DDL, `ALTER SYSTEM`, or any write against a real database without the user's explicit go — Claude prepares the statements, the user runs them. `EXPLAIN ANALYZE` on INSERT/UPDATE/DELETE executes the write: ask for a rolled-back transaction or a copy.
- NEVER assume engine, version, or deployment type. Missing → `[확인 필요: 엔진/버전/배포 유형]` and no parameter recommendation until the baseline arrives. Managed databases (RDS, Cloud SQL, Aurora) have no `ALTER SYSTEM` or `my.cnf`; parameter groups only.
- NEVER propose more than one change per round — two changes at once make the after-numbers unattributable. Use `CONCURRENTLY` for PostgreSQL indexes; no redundant indexes.
- Goal: each change has the user's baseline and after numbers side by side, or the run stops with what is missing. At most three change rounds.

# Database Optimizer

Server-side tuning driven by the user's own plan and metrics — one measured change at a time.

**Not for** rewriting a slow query (develop:sql-pro) or pool exhaustion (develop:connection-pool-tuner).

## Process

1. **Triage.** Confirm engine + version, deployment type, and whether the user has a direct connection. Missing → mark and ask once in one line.
2. **Baseline.** Ask for `EXPLAIN (ANALYZE, BUFFERS)` of the slow statement and cache/lock metrics (a `psql`/`mysql` session via Bash only if the user connected one and said go). Use `sequential-thinking`, if available, to hold the order baseline → change → verify.
3. **Locate the bottleneck** from the quoted plan nodes: seq scan, stale stats (estimate vs actual rows), spill to disk, cache misses, lock waits. Catalog: `references/explain-patterns.md`, `references/query-optimization.md`; engine topics in the other `references/` files.
4. **Design one change** — index, statistics, config, or partitioning — with its rollback. Prepare the statement; the user runs it.
5. **Validate.** Ask for the after-plan and metrics; compare with the baseline. Worse or replication lag up → roll back. Next round only after the comparison; third round without improvement → stop and report.

## Output Template

```
Baseline: <quoted node, time, buffers hit/read — or [확인 필요: EXPLAIN]>
Bottleneck: <node/metric quote → cause>
Change: <statement or parameter — rollback> (user runs; not executed)
After: <user's numbers> or pending
Monitoring: <metric to watch>
Verdict: <n> changes proposed, <n> with baseline and after, <n> marked [확인 필요]
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Reads your EXPLAIN and names the bottleneck node | Provide EXPLAIN output and engine, version, deployment type |
| Prepares one index or parameter change with rollback | Run it (index DDL, `ALTER SYSTEM`, or parameter group) in a safe environment |
| Compares baseline and after | Confirm the improvement on production-scale data |

## Related Skills

- `develop:sql-pro` — rewriting slow queries when the server is configured correctly
- `develop:connection-pool-tuner` — pool sizing after server config is validated
- `develop:sre-engineer` — monitoring and alerting on database golden signals
