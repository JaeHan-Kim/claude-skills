# Testing Workflow — map, entry points, ownership

## Overview

```
[1] Test-Driven Development
     Write failing test → minimal code → refactor
        ↓
[2] Test Coverage Strategy
     Audit coverage gaps → test pyramid → test plan
        ↓
[3] Flaky Test Elimination
     Triage → root cause → fix → CI hardening
```

## When to use / skip

| Use | Skip |
|-----|------|
| Starting a new feature with no tests | Adding a single test to already-covered code |
| Test suite exists but has no coverage strategy | Consistent (non-flaky) test failures — those are bugs |
| CI is failing intermittently due to flaky tests | Quick one-off unit test request |

## Step entry phrases

- Step 1: "Step 1 시작" or "TDD로 이 기능 개발해줘"
- Step 2: "Step 2 시작" or "테스트 커버리지 분석하고 전략 잡아줘"
- Step 3: "Step 3 시작" or "flaky test 원인 찾고 고쳐줘"

## State tracking

Tell Claude which step you are at and it joins there: "커버리지부터" → Step 2; "flaky test만 봐줘" → Step 3.
A step whose Skip-if condition holds is skipped and the next step is offered.

## Who does what per step

| Claude | You |
|--------|-----|
| Writes failing tests with clear names (Step 1) | Confirm the test tests the right behavior |
| Writes minimal passing implementation (Step 1) | Run tests and verify pass/fail as expected |
| Coverage gap analysis, test plan scaffolding (Step 2) | Provide existing test files and coverage reports |
| Flakiness root cause + fix patterns (Step 3) | Run the failing test 20 times in isolation to confirm |
| CI config recommendations (Step 3) | Wire fixes and configure CI pipeline |
