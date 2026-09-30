---
name: clean-code
description: >-
  Use when code is hard to read, too long, or unclear in intent and needs review or refactoring. Triggers: "리팩토링", "코드 가독성", "함수가 너무 길어", "clean code", "review this code".
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
scenarios:
  - "review this code for quality"
  - "refactor this function — it's too long"
  - "how should I name this variable?"
  - "이 코드 리팩토링해줘"
  - "코드 가독성이 너무 낮아"
  - "함수가 너무 길고 복잡해"
effort: high
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 코드 스멜 탐지와 리팩토링 우선순위 판단이 더 정확해집니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER rewrite the whole file to make it "clean" — fix only the smells you listed. A drive-by rewrite buries the real fix in a diff nobody can review and breaks behaviour nobody asked to touch.
- ALWAYS count smells by category with `file:line` quotes, never rate the code with an adjective or a score. A 0–10 score the author gives their own reading cannot be recounted.
- ALWAYS take "tests still pass" from the test run's output, not from your reading of the diff. Refactors that "obviously" preserve behaviour are where regressions hide.
- NEVER guess what unclear code is meant to do. Mark it `[확인 필요: 의도]` and leave that code alone — a refactor built on a guessed intent changes behaviour silently.
- Goal: every listed smell is fixed or explicitly left with a reason, and the test run is green. Stop after two fix rounds and report what remains.

# Clean Code

Code is read ten times for every time it is written. This skill finds what makes it slow to read and fixes that, and only that.

**Not for** layer or dependency decisions (develop:clean-architecture) or domain modelling (develop:domain-driven-design).

## Process

1. **Intake.** Get the code or diff. If none is attached, read the repo file the user named; if no file is named, ask in one line which one. Find the test command before touching anything.
2. **Baseline.** Run the tests. No tests → say so, mark `[확인 필요: 테스트 없음]`, and limit changes to renames and extractions.
3. **Find smells.** Use `think-tool`, if available, to rank them by reading cost. Quote each one with `file:line` under names, functions, comments, errors, or tests. Load `references/framework.md` for the catalog and the `references/` file for that category.
4. **Fix** the highest-cost smells first with a before/after snippet. One smell per change.
5. **Verify.** Re-run the tests; paste the exit status. Re-count the smells you listed. Two rounds without a green run → stop and report.

## Output Template

```
Smells found: <n> (names <a> · functions <b> · comments <c> · errors <d> · tests <e>)
| # | file:line | smell (quote) | fix |
Before/after: <one snippet per fixed row>
Left alone: <smell — reason, or "none">
Tests: <command> → <exit status>
Verdict: <fixed> of <n> smells fixed, tests <green | red | not run>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Quotes each smell with file:line and proposes a minimal fix | Share the code or diff and confirm the intent behind unclear code |
| Runs the tests before and after | Decide which left-alone items are worth a follow-up |
| Leaves unrelated problems unfixed and lists them | Review with a teammate and merge |

## Related Skills

- `develop:clean-architecture` — layer structure and the dependency rule
- `develop:domain-driven-design` — domain modelling and ubiquitous language
- `develop:test-master` — broader test generation
- `develop:test-driven-development` — test-first workflow
