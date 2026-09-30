---
name: connection-pool-tuner
description: >-
  Use when connections time out, pool exhaustion errors appear, or latency spikes under traffic and the pool (HikariCP, pgBouncer) needs diagnosis and tuning. Triggers: "커넥션 풀 고갈", "HikariCP 설정", "pool exhausted", "connection timeout".
effort: high
scenarios:
  - "Our application is getting 'connection pool exhausted' errors under load"
  - "Help me tune HikariCP settings for a Spring Boot service"
  - "Database connections are timing out — check our pool configuration"
  - "커넥션 풀이 고갈되면서 DB 연결 오류가 나"
  - "HikariCP 설정을 최적화해줘"
compatibility:
  optional:
    - sequential-thinking
  remote_mcp_note: >-
    sequential-thinking은 풀 크기를 제안하기 전에 증상 → 원인 진단을 먼저 끝내도록 순서를 강제합니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER raise `maximumPoolSize` before the user's active / pending / timeout numbers show the pool, not a slow query, is the bottleneck. A bigger pool in front of a saturated database just queues more work there and turns pool timeouts into database outages.
- NEVER run DDL, or any write, against a real database without the user's explicit go — Claude prepares config snippets and any statement; the user applies them.
- NEVER assume DB server specs or latency figures. Core count, disk type, P99 query time missing → `[확인 필요: DB 코어 수/디스크 유형]` / `[확인 필요: P99]` and stop. The sizing formula is a PostgreSQL-oriented starting point, not a law; say so when citing it.
- ALWAYS read numbers from the user's metrics (`hikaricp.connections.*`, `pg_stat_activity`, logs), never from the symptom's name.
- Goal: a user-supplied criterion (for example pending == 0 sustained and no timeouts at the user's peak) is met, or the run stops with what is missing. At most three tuning rounds.

# Connection Pool Tuner

Tunes a pool from the user's own pool metrics, after ruling out the query as the cause.

**Not for** slow SQL as the root cause (develop:sql-pro) or server memory/IO config (develop:database-optimizer).

## Process

1. **Intake.** Get current pool settings, the error text, and active / idle / pending / timeout numbers. Missing → mark and ask once in one line. Use `sequential-thinking`, if available, to finish diagnosis before any size is proposed.
2. **Diagnose.** Match the symptom below and quote the number that supports it. A slow query holding connections → hand to `develop:sql-pro`.
3. **Size** only with the user's real specs, using the starting-point formula in `references/pool-config.md`; otherwise mark `[확인 필요: DB 코어 수/디스크 유형]`.
4. **Configure** `maximumPoolSize`, `minimumIdle`, `connectionTimeout`, `maxLifetime` (shorter than the firewall/DB timeout), `leakDetectionThreshold` (2x the user's P99). Snippets and pgBouncer modes: `references/pool-config.md`.
5. **Monitor.** Name the metrics and the alert (`pending > 0` sustained). The user applies the change and reports the numbers under load; not met after three rounds → stop and report.

| Symptom | Likely Cause | Investigation |
|---------|-------------|---------------|
| `Connection timeout` under load | Pool too small, or slow queries holding connections | Active vs max; slow queries holding connections |
| Many idle connections at DB | Pool max too large | `idleTimeout`, `minimumIdle` |
| Slow response at traffic spikes | New connections created under load | `minimumIdle` gap; pre-warm the pool |
| `Connection leak detected` warnings | Code not returning connections | Leak detection; audit acquisition paths |
| DB CPU spikes with few active connections | N+1 queries holding connections | Profile queries; transactions spanning HTTP requests |
| Errors after DB failover | Stale connections in pool | Connection validation; `keepaliveTime` |

## Output Template

```
Symptom: <matched row> — evidence: <quoted metric or log line, or [확인 필요: …]>
Bottleneck: pool | query | database — <why>
Settings: <property: current → proposed, rationale> (user applies; not executed)
Monitor: <metric and alert>
Mistake check: <common mistakes from references/pool-config.md found in current config>
Verdict: <n> settings changed, <n> backed by your metrics, <n> marked [확인 필요]
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Names the bottleneck from your metrics and proposes settings | Provide DB core count, disk type, current pool settings, and metrics |
| Generates the HikariCP or pgBouncer snippet and the alert metrics | Apply the settings and observe under real load |
| Checks your config against the common-mistakes list | Decide recovery targets and wire alerts to your monitoring |

## Related Skills

- `develop:database-optimizer` — server-level tuning after the pool is correct
- `develop:sql-pro` — slow query rewriting when the pool is sized right
- `develop:circuit-breaker-tuner` — circuit breakers alongside the pool against cascading failure
