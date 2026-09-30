---
name: performance-profiling-optimization
description: >-
  Use when something is slow, leaking, or saturated and you need the bottleneck found and proven fixed with before/after numbers. Triggers: "느려졌어", "프로파일링", "메모리 누수", "CPU 병목", "profile this", "performance regression".
effort: high
scenarios:
  - "Our API response times degraded after the last deploy — help me profile and fix it"
  - "Profile this Java service to find memory leaks and CPU hotspots"
  - "Application throughput dropped by 40% — systematic performance investigation needed"
  - "배포 후 API 응답 시간이 느려졌는데 원인을 찾아줘"
  - "메모리 누수와 CPU 병목을 프로파일링해줘"
compatibility:
  optional:
    - datadog
  remote_mcp_note: >-
    datadog MCP가 있으면 APM 스팬과 메트릭에서 배포 전후의 P50/P95/P99를 직접 조회해 베이스라인과 검증 수치를 얻을 수 있습니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER name a bottleneck from symptoms alone. "Probably the DB" sends a week into an index that was never the problem — the name comes from profiler, trace, or query output the user's run produced.
- ALWAYS capture the baseline (P50/P95/P99, error rate, CPU, heap, RPS) before touching anything. A fix with no "before" cannot be shown to have worked.
- NEVER supply a missing baseline, load profile, or environment detail. Mark it `[확인 필요: 베이스라인]` and ask for the measurement — an assumed number makes the verdict unfalsifiable.
- ALWAYS change one thing per round and re-run the same load. Two changes at once leave you unable to say which one moved the number.
- ALWAYS take the after-number from a run, never from reasoning about the change.
- Goal: the target metric is met against the baseline under the same load, or three rounds are spent and the best measured result is reported with what is still unproven.

# Performance Profiling & Optimization

Measure first, hypothesize second, profile third, fix fourth, verify always.

**Not for** slow-query rewriting or index design (develop:database-optimizer), pool sizing (develop:connection-pool-tuner), or SLO and alert design (develop:sre-engineer).

## Process

1. **Baseline.** Ask for or measure P50/P95/P99, error rate, CPU %, heap used/max, GC frequency, thread-pool saturation and RPS at the time of the problem. Use `datadog` APM spans and metrics, if available, for the window around the degradation; otherwise use the user's pasted numbers or a `curl -w` timing via Bash. Missing item → `[확인 필요: 베이스라인]`. Close with a one-line problem statement and a numeric target; no target given → ask in one line.
2. **Hypothesize.** Pick the top 2–3 candidate causes from the symptom table in `references/profiling-guide.md`. They are hypotheses, not findings.
3. **Profile** the top hypothesis only, with the tool that fits the stack, run via Bash where the user allows it, otherwise handed to them: async-profiler or `jcmd` (JVM), py-spy (Python), perf (Linux), strace (syscalls), curl timing (network). Commands and reading guides are in `references/profiling-guide.md`. Quote the profiler output that confirms or kills the hypothesis.
4. **Fix.** One change, with the reason. The user applies it.
5. **Verify.** Re-run the same load and compare to the baseline in a before/after table. Met → add a regression test or load test that would fail if the number regresses, so the fix cannot silently recur, then stop. Not met and rounds < 3 → back to step 2 with the new evidence. Third round not met → stop and report.

## Output Template

```
Problem: <one line with baseline numbers>
Target: <metric ≤ value>
Evidence: <profiler / trace output quoted, tool + command>
Change: <one change, reason>
Guard: <regression test or load test added, or [확인 필요]>
| metric | before | after |
Open: <k> × [확인 필요: …]
Verdict: <met | not met> target, <n> rounds
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Sets the baseline and states the problem in one line | Provide metrics and the target |
| Forms hypotheses and names the profiling command | Run the profiler in your environment and share the output |
| Proposes one targeted change per round | Apply the change |
| Compares before/after numbers and states the verdict | Provide the post-fix metrics and accept or reject the verdict |

## Related Skills

- `develop:database-optimizer` — query and index bottlenecks
- `develop:connection-pool-tuner` — pool exhaustion and sizing
- `develop:circuit-breaker-tuner` — latency causing downstream cascades
- `develop:sre-engineer` — production profiling, SLOs, alerting
