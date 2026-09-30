---
name: flaky-test-analyzer
effort: high
description: >-
  Use when tests pass locally but fail in CI, pass some runs and fail others, or a test seems unreliable and the failure won't reproduce consistently. Triggers: "flaky test", "간헐적 실패", "CI에서만 실패".
scenarios:
  - "Our tests pass locally but randomly fail in CI — I need to fix these flaky tests"
  - "Help me diagnose why this test fails intermittently with a race condition"
  - "CI pipeline keeps red because of non-deterministic test failures"
  - "로컬에선 통과하는 테스트가 CI에서 랜덤으로 실패해"
  - "간헐적으로 실패하는 테스트 원인을 찾아줘"
compatibility:
  recommended:
    - think-tool
  optional:
    - sequential-thinking
  remote_mcp_note: >-
    think-tool이 있으면 간헐적 실패의 근본 원인을 더 체계적으로 추론합니다.
    sequential-thinking은 분류 없이 수정부터 들어가는 것을 막는 데 씁니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER add a sleep, a retry, or a quarantine before the cause is reproduced. A sleep moves the race to a slower CI machine and the test comes back red a week later, now with the evidence gone.
- ALWAYS state the failure category (from `references/triage-and-categories.md`) before proposing a fix — skipping triage is the primary failure mode.
- ALWAYS take "reproduced" and "fixed" from run output with a count (failures out of N runs). Claude cannot run CI; the user's run results are the evidence.
- NEVER name a cause the runs did not show. Cause unreproduced after the bounded reruns → `[확인 필요: 원인 미재현]`, propose logging and a next experiment, and stop.
- NEVER commit a "re-run on failure" workaround without a ticket for the root cause.
- Goal: one category, one cause backed by a failing-run count, one fix backed by a passing-run count. Rerun bound: 20 runs per condition (isolation, ordering, parallel); hitting it without a failure is the `[확인 필요]` result.

# Flaky Test Analyzer

Turns "it fails sometimes" into a category, a reproduced cause, and a fix checked by reruns.

**Not for** a test that fails every time — that is a bug — or writing new tests (develop:test-master) or test-first development (develop:test-driven-development).

## Process

1. **Triage first.** Identify the failure category from the symptom and the user's log. With `sequential-thinking`, if available, work steps 1–5 in order.
2. **Reproduce in isolation.** The user runs only the failing test 20 times and reports failures out of 20.
3. **Reproduce with ordering, then parallel.** Run it after each other test; then in parallel. Same bound: 20 runs each.
4. **Add logging.** Timestamps, thread names, and state snapshots at failure time. Use `think-tool`, if available, to reason from the logs to a cause before naming one.
5. **Check nondeterministic inputs and cleanup.** Search for `new Date()`, `Math.random()`, `UUID.randomUUID()`, `System.currentTimeMillis()`; verify `@AfterEach` teardown, unclosed streams, un-stubbed mocks.
6. **Fix, then verify by rerun.** Fix patterns: `references/flaky-fix-patterns.md`. The user re-runs 20 times; report failures out of 20.

## Output Template

```
Test: <name>
Category: <from triage> — symptom: <quote from log>
Reproduced: <n> failures in <20> runs (<isolation | ordering | parallel>) — or [확인 필요: 원인 미재현]
Root cause: <cause> — evidence: <log line or run count>
Fix: <code snippet>
Verified: <n> failures in 20 runs after the fix
Prevention rule: <one rule for the suite>
CI config: <flag or setting that would catch this class earlier>
Verdict: <n> of <m> flaky tests fixed and verified, <k> unreproduced
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Identifies the failure category from symptoms | Provide the test code and failure log |
| Explains why the cause fails intermittently | Run the test 20 times per condition and report counts |
| Provides the specific fix pattern (waitFor, Clock injection, etc.) | Implement the fix and decide whether to quarantine |
| Suggests cleanup patterns and CI flags (random ordering) | Configure the CI pipeline |

## Related Skills

- `develop:test-master` — new tests with flakiness prevention built in
- `develop:test-driven-development` — TDD patterns that reduce flakiness by design
- `develop:chaos-engineer` — intentionally testing failure behaviour
