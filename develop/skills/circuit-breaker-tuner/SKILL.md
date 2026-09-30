---
name: circuit-breaker-tuner
effort: medium
description: >-
  Use when a slow or failing downstream causes latency, thread exhaustion, or outages and breakers, bulkheads, timeouts need tuning. Triggers on "서킷 브레이커", "임계값 설정", "circuit breaker", "cascading failure".
scenarios:
  - "Our circuit breaker is tripping too often and causing unnecessary service disruptions"
  - "Help me tune the circuit breaker thresholds for our payment service"
  - "Circuit breaker keeps opening on false positives, need to configure proper settings"
  - "서킷 브레이커가 너무 자주 열려서 서비스 장애가 발생해"
  - "서킷 브레이커 임계값 설정을 도와줘"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 failureRateThreshold와 waitDuration 트레이드오프를 더 정확하게
    평가합니다. Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER emit thresholds without the dependency's measured latency and recovery time; a default copied from a blog post opens on noise or never opens.
- Missing latency, recovery time, or error mix: write `[확인 필요: ○○]` in the config comment and stop at that value; never guess it.
- Every threshold carries a one-line rationale tied to a measured number.
- The pass that sets thresholds never declares them verified; the load test or chaos run that confirms them belongs to the user or develop:chaos-engineer.

# Circuit Breaker Tuner

A breaker that opens on a single slow call is as bad as none. Numbers come from the dependency, not from defaults.

Goal: a config for each named dependency where every value has a measured basis or a `[확인 필요]` marker, plus a fallback, a bulkhead, and a state-change alert. Stop when the checklist is counted; confirmation is the user's run.

**Not for** slow SQL or missing indexes (develop:database-optimizer), chaos experiment design (develop:chaos-engineer), pool sizing (develop:connection-pool-tuner).

## Process

1. **Identify the dependency** -- Typical latency, p99, recovery time. Read metrics or config first; ask one line for what is absent.
2. **Set state parameters** -- `failureRateThreshold`, `waitDurationInOpenState`, `minimumNumberOfCalls`; use think-tool for the false-positive vs slow-detection tradeoff.
3. **Sliding window** -- COUNT_BASED or TIME_BASED, with the reason.
4. **Fallback** -- What callers receive when OPEN.
5. **Bulkhead** -- Cap concurrent calls so the pool survives before the circuit opens.
6. **Monitoring** -- Alert on CLOSED to OPEN transitions.
7. **Count the checklist** -- Mark each item with its evidence; hand the confirming load test to the user.

Starting points: 50% failure rate, `minimumNumberOfCalls` 10, wait slightly longer than downstream recovery (5-15 s fast, 60-120 s operator-driven). 4xx belong in `ignoreExceptions`; HTTP timeout must exceed `slowCallDurationThreshold`. See `references/resilience4j-config.md`, `references/fallback-patterns.md`, `references/metrics-alerting.md`.

## Output Template

1. Resilience4j YAML or code with commented rationale
2. Fallback method implementation
3. Bulkhead config
4. Alert rule for state changes
5. Test scenario for OPEN to HALF_OPEN to CLOSED, for the user to run
6. Verdict line

Checklist: `minimumNumberOfCalls` >= 10; threshold calibrated to this dependency; slow-call threshold consistent with client read timeout; open wait longer than recovery; 4xx ignored; fallback defined; bulkhead present; transition alerts wired.

Tag each config value with a `# basis: <measured number>` comment; count with `grep -c '# basis:' <config file>` and quote that command, or have the user confirm the count. Never tally by re-reading the checklist.

```
Verdict: N of 8 checklist items have evidence; K values marked [확인 필요]; load test run by user: no
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Recommends thresholds with rationale | Confirm recovery time from runbooks and metrics |
| Generates Resilience4j or Spring Boot config | Apply it in your environment |
| Writes fallback stubs | Fill in the real degraded-mode logic |
| Flags common mistakes in current config | Test the circuit under load |
| Explains state transitions | Verify alert routing reaches the right team |

## Related Skills

- `develop:connection-pool-tuner` -- pool exhaustion often co-occurs with missing breakers
- `develop:chaos-engineer` -- confirm breaker behavior with controlled fault injection
- `develop:transaction-boundary-reviewer` -- wide transactions compound cascading failure
