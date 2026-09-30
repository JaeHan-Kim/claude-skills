---
name: transaction-boundary-reviewer
description: >-
  Use when data is inconsistent after failures, two writes must commit or fail together, or transactions cause lock waits and timeouts. Triggers: "트랜잭션 경계", "데이터 정합성", "@Transactional 검토", "review transaction boundaries".
effort: high
scenarios:
  - "Data is inconsistent after failures — review our transaction boundaries"
  - "Two writes must succeed or fail together — is this @Transactional correct?"
  - "Our transactions hold locks and time out under load"
  - "장애 후 데이터가 불일치해 — 트랜잭션 경계를 검토해줘"
  - "분산 트랜잭션으로 인한 데이터 정합성 문제를 해결해줘"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 이상 현상(anomaly)을 이름 붙이고 코드 경로와 대응시키는 판단이 더 정확해집니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER recommend an isolation level (or `SERIALIZABLE`) before naming the specific anomaly and the code path that produces it. "Raise the isolation" as a blanket fix trades one bug for deadlocks and retries, and leaves a wide transaction or a missing lock untouched.
- NEVER run DDL, or any write, against a real database without the user's explicit go — Claude reviews code and prepares statements (locks, `@Version` columns, outbox tables); the user runs them.
- NEVER infer code you were not shown. Callers, propagation, proxy self-invocation, repository code, or the DB's default isolation not pasted → `[확인 필요: 호출 경로]` / `[확인 필요: 격리 수준 설정]`. A boundary guessed from method names is how a review approves a transaction that never opens.
- ALWAYS mark engine-dependent claims (lock behaviour, phantom handling, `SELECT FOR UPDATE`) as such; defaults differ between PostgreSQL and MySQL.
- Goal: each transaction path the user named has its at-risk ACID property and quoted evidence, or a `[확인 필요]`. Review only the paths named; list the rest as unreviewed.

# Transaction Boundary Reviewer

Finds where a transaction is too wide, too narrow, or absent — by quoting the user's code, not by prescribing a level.

**Not for** slow SQL (develop:sql-pro) or pool exhaustion as the root cause (develop:connection-pool-tuner).

## Process

1. **Intake.** Get the service method and repository code for each path the user named, plus the symptom. Read the repo before asking; missing code → ask once in one line.
2. **Name the ACID property at risk** — Atomicity, Isolation, Consistency, or Durability — and the anomaly (partial write, lost update, dirty read, …). Use `think-tool`, if available, when two anomalies fit. No anomaly nameable from the evidence → `[확인 필요]`.
3. **Map the boundary.** What runs inside `@Transactional`? External I/O? Propagation, proxy self-invocation, `rollbackFor`. Quote each line.
4. **Find anti-patterns** — wide transaction, N+1 inside, missing rollback, read-modify-write without lock or version, cross-service write without Outbox/Saga. Catalog, code, and tables: `references/anti-patterns.md`; Outbox and Saga code: `references/distributed-patterns.md`.
5. **Fix.** Narrow the scope or add the lock/version; choose the lowest isolation level that prevents the named anomaly and say why. Cross-service → Outbox or Saga, with the compensation logic left to the user.

## Output Template

```
ACID at risk: <property> — anomaly: <name> (path: <method>)
| # | anti-pattern | quote from your code | fix |
Corrected: <code or pattern per row>
Isolation: <level for the named anomaly — rationale> or none needed
Unreviewed: <paths or [확인 필요: …]>
Verdict: <n> anti-patterns found, <n> quoted from your code, <n> marked [확인 필요]
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Quotes the boundary and names the anomaly it produces | Provide service and repository code and the DB's isolation setting |
| Proposes narrowed scope, lock, version, Outbox, or Saga | Confirm concurrent access patterns and test under load |
| Prepares any schema statement (outbox table, version column) | Run it, implement the relay, and write the real compensation logic |

## Related Skills

- `develop:spring-boot-engineer` — implementing the corrected `@Transactional` patterns
- `develop:microservices-architect` — cross-service transaction design
- `develop:circuit-breaker-tuner` — wide transactions compound cascading failure
- `develop:connection-pool-tuner` — wide transactions can exhaust the pool
