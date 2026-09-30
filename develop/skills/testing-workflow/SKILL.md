---
name: testing-workflow
description: >-
  Use when building a complete, stable test suite from scratch: TDD, then coverage strategy, then flaky-test elimination. Triggers: "testing workflow", "테스트 전체 프로세스", "TDD부터 커버리지까지", "CI 테스트 안정화".
type: workflow
theme: engineering
effort: high
scenarios:
  - "testing workflow 전체 돌려줘"
  - "TDD부터 커버리지 전략까지 단계별로 해보자"
  - "full test cycle from scratch"
  - "run the whole testing process on this module"
  - "테스트 체계 제대로 잡고 싶어"
estimated_time: "2-8 hours (full), 30-120 min per step"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool은 2단계 커버리지 갭의 우선순위 판단에 유효합니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER report a step done from your own reading of the code or the diff. Only a run's output counts: a failing run that then passes (Step 1), a coverage report you did not write (Step 2), N reruns with a count (Step 3). "Looks covered" and "should be stable" are how a green-looking suite ships untested.
- ALWAYS mark a missing fact `[확인 필요: ○○]` (test command, coverage tool, CI log) and stop at that step — a guessed command produces a guessed result.
- ALWAYS offer the next step, never start it: the user chooses to continue, skip, or stop after each step.
- ALWAYS skip a step only on its Skip-if condition, quoted back to the user with the evidence.
- Goal: each step you ran closes on its own evidence line, and the verdict counts the steps done, skipped, and open. One pass through the 3 steps; a step that cannot finish is reported open, not retried endlessly.

# Testing Workflow

Test quality in order: write first, then decide where coverage matters, then make CI trustworthy. The map, entry phrases, and skip table are in `references/workflow-map.md`.

**Not for** a single test or one intermittent failure (develop:test-master, develop:flaky-test-analyzer) or the full architecture-to-incident cycle (develop:dev-quality-workflow).

## Process

1. **Test-first (develop:test-driven-development).** Input: requirements or acceptance criteria. Output: a suite built test-first, each test with its recorded failing run. Skip if the feature is a throwaway prototype, or you are adding tests to untested code (go to 2).
2. **Coverage strategy (develop:test-master).** Input: the module from step 1, or existing code. Use `think-tool`, if available, to rank coverage gaps by risk. Output: gap report from the user's coverage run, test pyramid, test plan. Skip if coverage targets are met and a current plan exists.
3. **Flaky-test elimination (develop:flaky-test-analyzer).** Input: failing CI logs or the flaky list from step 2. Output: cause per test with evidence, fix, prevention rule. Skip if CI passes consistently with no rerun workarounds.

## Output Template

```
Step 1 TDD:      <ran | skipped: reason> — <n> tests, <n> with a failing run recorded
Step 2 Coverage: <ran | skipped: reason> — <n> gaps, <n> covered by the plan
Step 3 Flaky:    <ran | skipped: reason> — <n> flaky tests, <n> root causes confirmed by rerun
Open: <[확인 필요] items, or "none">
Verdict: <n> of 3 steps done, <n> skipped, <n> open
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Runs each step's skill and reports its evidence line | Decide whether to continue, skip, or stop after each step |
| Quotes the Skip-if evidence before skipping | Supply test command, coverage report, CI logs |
| Lists open `[확인 필요]` items in the verdict | Run the reruns and wire CI fixes |

## Related Skills

- `develop:test-driven-development`, `develop:test-master`, `develop:flaky-test-analyzer` — the three steps
- `develop:dev-quality-workflow` — before this: the full cycle including architecture and docs
- `develop:performance-profiling-optimization` — after this: once the suite is green and stable
