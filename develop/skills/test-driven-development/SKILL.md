---
name: test-driven-development
effort: high
description: >-
  Use when tests must prove a fix or feature works, not just pass: TDD, red-green-refactor, falsifiable tests. Triggers: "TDD", "테스트 먼저 작성", "test-first", "red-green-refactor", "이 테스트가 버그를 잡는지".
references:
  - references/testing-anti-patterns.md
  - references/tdd-catalog.md
scenarios:
  - "let's do TDD on this feature"
  - "prove this test would actually catch the bug"
  - "TDD로 개발해줘"
  - "이 테스트가 진짜 버그를 잡는지 증명해줘"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 RED 실패 원인 판별과 REFACTOR 단계의 동작 변경 여부
    판단이 더 정확해집니다. Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를
    추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER accept a green run as proof without the failing run before it. A test never watched to fail can pass because it asserts nothing, and the suite then guards a bug it cannot see. The pasted RED output is the evidence; your prediction of it is not.
- ALWAYS write the failing test before any production code. Code that arrived first is deleted and rebuilt from the test — keeping it "for reference" is the same violation.
- ALWAYS name, before the run, the exact production change that would make the test fail (the falsifiability probe). A test you cannot name a breaking change for is one you do not understand yet.
- NEVER grade your own probe. The command output decides RED and GREEN; the user confirms the named breaking change is real and specific.
- ALWAYS make the smallest change that turns RED to GREEN, and refactor only on green.
- ALWAYS mark a missing fact `[확인 필요: 테스트 명령]` and stop; a guessed command yields a guessed result.
- Goal: each behaviour has a RED Evidence Record whose observed failure matches the named reason, then a GREEN run. A failure that does not match the prediction: stop and re-diagnose once, then report it open.

# Test-Driven Development (TDD)

A passing suite is not evidence. A passing suite plus a recorded failure that happened for the predicted reason is. Dual-mode table (solo vs harness), Iron Law, code samples, Good Tests, When Stuck, Red Flags, Debugging Integration: `references/tdd-catalog.md`.

**Not for** adding tests to existing untested code (develop:test-master) or an intermittent failure (develop:flaky-test-analyzer). Skip for throwaway prototypes, generated code, config files.

## Process

Skim `references/testing-anti-patterns.md` before the first RED: it pre-screens for mock traps.

1. **RED — one failing test.** One behaviour, a name that reads as a sentence about behaviour, real collaborators (mock only what cannot run).
2. **Probe.** Write the one-sentence breaking change ("if the failure counter is removed") before running. Cannot → stop and clarify the behaviour.
3. **Verify RED.** Run the test; paste the output. Use `think-tool`, if available, to ask whether the failure text is the predicted reason (feature absent) or a typo, bad import, or syntax slip; only the former is a valid RED. Passes at once → rewrite the test. Errors instead of failing → fix and re-run. Record test name, breaking change, observed failure reason.
4. **GREEN.** Smallest code that passes; no options, no generality, no "while I'm here".
5. **Verify GREEN.** Run and paste. Use `think-tool`, if available, to ask whether it passed because the behaviour is implemented or because an assertion was loosened. Optional: apply the named breaking change, re-run — still passing means fix the test.
6. **REFACTOR on green.** Use `think-tool`, if available, to classify each planned edit as structure-only or behaviour-changing; a behaviour change needs its own RED. Re-run after.
7. **Repeat** for the next behaviour; two failed fix rounds on one test → stop and report.

## Output Template

```
Behaviour: <one line>
Test: <name>
Probe (pre-run): <breaking change>
RED: <command> → <observed failure reason> — matches probe: <yes | no>
GREEN: <command> → <exit status>
Refactor: <structure-only edits, or "none">
Queued: <next behaviour>
Verdict: <n> of <m> cycles with a matching RED record, <n> GREEN
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Writes the failing test, states the probe, runs it, pastes the output | Confirm the probe names a real, specific breaking change |
| Fills the RED Evidence Record from actual command output | Spot-check that the observed failure reason matches the prediction |
| Writes the minimal GREEN code and classifies refactor edits | Approve refactor direction; decide go/no-go on discarding pre-written code |
| Flags red-flag language the moment it appears | Run verification per `completion:verification-before-completion` in solo mode |

## Related Skills

- `completion:verification-before-completion` — the solo-mode evidence gate GREEN defers to
- `harness:harness` — the harness-mode QualityGate this evidence trail feeds
- `develop:test-master` — tests for existing untested code
- `develop:flaky-test-analyzer` — intermittent test failures
