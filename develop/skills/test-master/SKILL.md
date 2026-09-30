---
name: test-master
effort: high
description: >-
  Use when writing, improving, or auditing tests — unit, integration, E2E, performance, security — or analyzing coverage gaps and producing a test plan. Triggers: "테스트 작성", "단위 테스트", "커버리지 분석", "write tests", "test plan".
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: quality
  role: specialist
  scope: testing
  output-format: report
  related-skills: test-driven-development, flaky-test-analyzer
scenarios:
  - "write unit tests for this service"
  - "analyze test coverage"
  - "generate a test plan"
  - "이 코드에 테스트 추가해줘"
  - "테스트 커버리지 분석해줘"
  - "통합 테스트 어떻게 짜야 해?"
compatibility:
  recommended:
    - think-tool
  optional:
    - sequential-thinking
  remote_mcp_note: >-
    think-tool이 있으면 플레이키 실패 원인 추론과 커버리지 갭 분석이 더 정확해집니다.
    sequential-thinking은 범위·전략 확정 전 테스트 코드 작성을 막는 데 씁니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER hand over a generated test you have not seen run. A test written to pass against the current code mirrors the implementation: it stays green when the behaviour breaks, and the suite then reports coverage that protects nothing. Paste each test's run output; a test never run is `[확인 필요: 미실행]`.
- ALWAYS assert a specific outcome and cover the error path, not just the success branch; mock external dependencies, never use production data, keep every test independently runnable (examples and the full rule list: `references/quick-start.md`).
- ALWAYS take coverage numbers from the user's coverage run. No report available → mark `[확인 필요: 커버리지 리포트]`; never estimate a percentage from reading the code.
- NEVER rerun a flaky test until green. Classify the failure, then hand a recurring one to develop:flaky-test-analyzer.
- Goal: every test delivered has a recorded run, every gap in the plan has a severity, and the report closes on a recountable verdict. One fix round per failing test; then report it open.

# Test Master

Finds what is untested and writes tests that can fail. Scope first, strategy second, code last.

**Not for** test-first development of a new feature (develop:test-driven-development) or one intermittent failure (develop:flaky-test-analyzer).

## Process

1. **Define scope.** Get the code and the test command from the repo; ask one line only if the repo does not answer. Identify the testing types that apply.
2. **Create strategy.** Functional, performance, and security perspectives; framework; coverage targets. Use `sequential-thinking`, if available, to finish steps 1 and 2 as separate steps before any test file is written.
3. **Write tests.** Specific assertions, edge cases, error paths. Load the `references/` file for the type (table below).
4. **Execute.** Run the tests and paste the output. On failure classify it: assertion error vs environment/flakiness, fix the root cause, re-run once. For a flaky failure use `think-tool`, if available, to reason through the failure chain before naming a cause; then isolate ordering dependencies and async handling.
5. **Report.** Findings with severity and a fix each; gaps against the user's coverage report; one row per delivered test with its run result.

## Reference Guide

Load detailed guidance based on context:

<!-- TDD Iron Laws and Testing Anti-Patterns adapted from obra/superpowers by Jesse Vincent (@obra), MIT License -->

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Unit Testing | `references/unit-testing.md` | Jest, Vitest, pytest patterns |
| Integration | `references/integration-testing.md` | API testing, Supertest |
| E2E | `references/e2e-testing.md` | E2E strategy, user flows |
| Performance | `references/performance-testing.md` | k6, load testing |
| Security | `references/security-testing.md` | Security test checklist |
| Reports | `references/test-reports.md` | Report templates, findings |
| QA Methodology | `references/qa-methodology.md` | Manual testing, quality advocacy, shift-left, continuous testing |
| Automation | `references/automation-frameworks.md` | Framework patterns, scaling, maintenance strategies |
| Automation Ops | `references/automation-operations.md` | CI/CD setup, team rollout, automation ROI |
| TDD Iron Laws | `references/tdd-iron-laws.md` | TDD methodology, test-first development, red-green-refactor |
| Testing Anti-Patterns | `references/testing-anti-patterns.md` | Test review, mock issues, test quality problems |

Quick-start example, MUST DO / MUST NOT rules, and the report sections: `references/quick-start.md`.

## Output Template

```
Scope: <what is tested, which types>
| # | test | type | run result |
Gaps: <n> (Critical <a> · High <b> · Medium <c> · Low <d>) — each with a fix recommendation
Coverage: <figure from the user's report, or [확인 필요: 커버리지 리포트]>
Verdict: <passed> of <total> delivered tests pass, <n> gaps open
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Generates test scaffolding and assertions, and runs them | Confirm test scope and edge cases |
| Identifies coverage gaps against your coverage report | Run coverage and share the report and failure output |
| Writes the test plan and ranks gaps by severity | Validate that tests match business intent and decide which gaps to accept |
| Suggests mocking strategies | Integrate tests into CI/CD |

## Related Skills

- `develop:test-driven-development` — TDD workflow (red-green-refactor cycle)
- `develop:flaky-test-analyzer` — diagnose intermittent test failures
- `develop:clean-code` — test code quality and readability
