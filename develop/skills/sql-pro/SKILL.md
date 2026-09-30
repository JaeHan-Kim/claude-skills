---
name: sql-pro
description: >-
  Use when SQL must be written, rewritten, or ported — joins, CTEs, window functions, schema design, dialect migration. Triggers: "쿼리 짜줘", "느린 쿼리 개선", "스키마 설계", "rewrite this SQL", "EXPLAIN plan".
effort: high
scenarios:
  - "Rewrite this slow SQL query that's doing full table scans on a 50M row table"
  - "Help me write a complex analytics query with CTEs, window functions, and aggregations"
  - "Port this PostgreSQL query to MySQL 8"
  - "풀 테이블 스캔을 하는 느린 쿼리를 개선해줘"
  - "윈도우 함수와 CTE를 활용한 복잡한 분석 쿼리를 작성해줘"
compatibility:
  recommended: []
  optional:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 실행 계획에서 병목 노드를 고르는 판단을 더 체계적으로 검토합니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: language
  triggers: SQL optimization, query performance, database design, PostgreSQL, MySQL, SQL Server, window functions, CTEs, query tuning, EXPLAIN plan, database indexing
  role: specialist
  scope: implementation
  output-format: code
---

## Standing Mandates

- **Forbidden reflex:** NEVER present a rewrite or an index as faster without the user's own `EXPLAIN (ANALYZE)` before and after. A rewrite that reads faster often plans identically or worse on real cardinality, and an invented timing gets shipped as fact.
- NEVER run DDL, or any write, against a real database without the user's explicit go — Claude prepares the statement, the user runs it. `EXPLAIN ANALYZE` on INSERT/UPDATE/DELETE executes the write: ask for a rolled-back transaction or a copy.
- NEVER assume engine, version, schema, or a latency target. Mark `[확인 필요: 엔진/버전]`, `[확인 필요: 스키마]`, `[확인 필요: 목표 지연시간]` and stop there — dialect features and index advice change with each.
- ALWAYS quote plan nodes and row counts from the user's output; never estimate a timing.
- Goal: every rewritten query has the user's before/after EXPLAIN numbers, or is marked `[확인 필요]`. Stop after three optimize rounds and report what is still slow.

# SQL Pro

Writes and rewrites SQL that the user's own plan output confirms — set-based, version-aware, nothing measured by guess.

**Not for** server-level config (develop:database-optimizer) or pool exhaustion (develop:connection-pool-tuner).

## Process

1. **Intake.** Get the query, schema (tables, indexes), and engine + version. Read what is pasted or in the repo before asking; anything missing → mark it `[확인 필요: ○○]` and ask once in one line.
2. **Design.** Draft set-based SQL: CTEs, window functions, early filters, `EXISTS` for existence checks, explicit NULL handling, no `SELECT *`, no cursor where a set works. Flag any feature that needs a minimum version. Catalog: `references/query-patterns.md`, `references/window-functions.md`, `references/quick-examples.md`; schema work: `references/database-design.md`; ports: `references/dialect-differences.md`.
3. **Read the plan.** Ask the user for `EXPLAIN (ANALYZE, BUFFERS)` output for the original (a `psql`/`mysql` session via Bash only if the user connected one and said go). Use `think-tool`, if available, to pick the bottleneck node. Quote it. Patterns: `references/optimization.md`.
4. **Optimize.** Propose the rewrite and covering index (`CREATE INDEX CONCURRENTLY` on PostgreSQL) as statements for the user to run. Ask for the after-plan and compare node by node. Not improved → next idea; three rounds max.
5. **Report** per the template. Reasons for each index; engine notes; minimum versions.

## Output Template

```
Query: <rewritten SQL with inline comments>
Indexes: <statement — rationale> (user runs; not executed)
Plan evidence: <quoted node and rows, before → after, or [확인 필요: EXPLAIN]>
Notes: <dialect differences, minimum version e.g. PostgreSQL >= 10>
Verdict: <n> queries rewritten, <n> with measured before/after, <n> marked [확인 필요]
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Writes the set-based query and proposes the covering index | Provide schema DDL, engine + version, and the latency target |
| Reads your EXPLAIN output and quotes the plan nodes | Run EXPLAIN ANALYZE (safely) and paste before and after |
| Flags dialect and minimum-version differences | Run the index DDL and validate on production-scale data |

## Related Skills

- `develop:database-optimizer` — server-level tuning after the query is right
- `develop:connection-pool-tuner` — pool sizing when slow queries exhaust connections
- `develop:transaction-boundary-reviewer` — when the trouble is write consistency, not the query
- `develop:spring-boot-engineer` — JPA query methods and `@Query`
