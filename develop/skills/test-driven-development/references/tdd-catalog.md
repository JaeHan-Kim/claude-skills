# TDD cycle catalog

Detail moved out of SKILL.md. The cycle itself is `## Process` there.

## Dual-Mode Operating Map

This skill runs the same cycle whether you're working alone or the harness engine owns the run. What changes is who checks the evidence and where it's checked.

| Step | Solo mode | Harness-engaged mode |
|---|---|---|
| RED | You write the falsifiability probe; the failing run's output, pasted, is the check — the user confirms it names a real breaking change | The probe is checked against SetGoal's acceptance criteria before Implement proceeds |
| GREEN | You run the verify command yourself before claiming done — see `completion:verification-before-completion` | The Test stage runs the verify command; QualityGate blocks completion claims without its output |
| evidence | You keep the RED Evidence Record in your own working notes as the receipt for "I watched it fail" | The RED Evidence Record is durable artifact for `harness:harness`'s QualityGate — missing or fabricated records fail the gate |

Not sure which mode you're in? If a harness pipeline invoked this skill, you're in harness mode — defer to its stage boundaries. Otherwise, default to solo mode and self-apply the same checks.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Code arrived before its test? Throw it away and rebuild from the test. Keeping it "for reference" or "to adapt" is the same violation wearing a different excuse — the fix is to not have it in front of you.

### RED — Write One Failing Test

Pick one behavior. Name the test after that behavior, not after the code path.

```typescript
test('opens the circuit after 3 consecutive failures', async () => {
  const breaker = new CircuitBreaker({ threshold: 3 });
  const failingCall = () => Promise.reject(new Error('down'));

  await breaker.attempt(failingCall).catch(() => {});
  await breaker.attempt(failingCall).catch(() => {});
  await breaker.attempt(failingCall).catch(() => {});

  expect(breaker.isOpen()).toBe(true);
});
```

**Requirements:** one behavior per test, a name that reads as a sentence about behavior, and real collaborators — reach for a mock only when a dependency can't be run in the test.

### Falsifiability Probe (REQUIRED)

Before you run the test, write down the exact production change that would flip it to failing. This is not optional and it is not a review of some earlier note — it's a fresh commitment you make for every RED test, right now, before GREEN exists:

1. **Name the breaking change.** One sentence: "if the threshold counter is removed" or "if `isOpen()` always returns false." Be specific enough that someone else could make that exact change.
2. **Run the test now**, before any implementation exists, and confirm it fails.
3. **Optional, after GREEN:** apply the named breaking change to the working implementation and re-run the test. If it still passes, the test was never testing what you thought — fix the test before moving on. If it fails as predicted, revert the change; that failure is your proof the test has teeth.

A test you can't name a breaking change for is a test you don't understand yet. Don't run it — go back and clarify what behavior it's supposed to pin down.

### RED Evidence Record

Every RED cycle produces one record — three fields, filled in as you go, not reconstructed afterward:

| Field | What goes here |
|---|---|
| Test name | `opens the circuit after 3 consecutive failures` |
| Breaking change named (pre-GREEN) | "removing the failure counter increment" |
| Observed failure reason | `TypeError: breaker.isOpen is not a function` — missing implementation, matches expectation |

Keep this record with the test, in a commit message, or in your working notes — wherever the harness-mode evidence gate or your own solo-mode discipline can find it later. An "observed failure reason" that doesn't match what you predicted means stop and re-diagnose before writing any implementation.

### Verify RED — Watch It Fail

**MANDATORY. Never skip.**

```bash
npm test path/to/test.test.ts
```

If think-tool is available, use it here: does the failure text match the reason recorded above — feature genuinely absent — or does it look like a typo, a bad import, a syntax slip? Only the former is a valid RED.

**Test passes immediately?** You're exercising code that already exists. Rewrite the test.

**Test errors instead of failing?** Fix the error, rerun, until the failure is the one you predicted.

### GREEN — Smallest Code That Passes

Write only enough to satisfy the test in front of you. Resist adding options, generality, or the "while I'm here" cleanup — that belongs in REFACTOR, and only if a test demands it.

```typescript
class CircuitBreaker {
  private failures = 0;
  constructor(private opts: { threshold: number }) {}

  async attempt<T>(fn: () => Promise<T>): Promise<T> {
    try {
      const result = await fn();
      this.failures = 0;
      return result;
    } catch (e) {
      this.failures++;
      throw e;
    }
  }

  isOpen(): boolean {
    return this.failures >= this.opts.threshold;
  }
}
```

### Verify GREEN — Watch It Pass

**MANDATORY.**

```bash
npm test path/to/test.test.ts
```

If think-tool is available, use it here: did the test pass because the behavior is now correctly implemented, or because an assertion got loosened on the way to green? Those look identical in a terminal and are not the same outcome.

### REFACTOR — Clean Up on Green Only

If think-tool is available, classify every planned edit as structure-only (rename, extract, dedupe) or behavior-changing before touching anything. Proceed only with the structure-only ones — a behavior-changing edit needs its own RED first.

Remove duplication, sharpen names, extract helpers. Tests stay green throughout; if one goes red mid-refactor, that edit wasn't structure-only after all.

## Good Tests

| Trait | Looks like | Doesn't look like |
|---|---|---|
| **Single-purpose** | One behavior; an "and" in the name means split it | `test('validates email and domain and whitespace')` |
| **Self-describing** | Name alone tells you what broke on failure | `test('test1')`, `test('works')` |
| **Intent-revealing** | Reads like the API you wish existed | Buries the contract under setup noise |

## When Stuck

| Symptom | Likely fix |
|---|---|
| Can't picture the test | Sketch the call you wish existed, write the assertion first, then fill in the setup |
| Test is fighting you | The design under test is fighting you — simplify the interface, not the test |
| Everything needs a mock | The code is too tightly coupled; inject the dependency instead |
| Setup dwarfs the assertion | Pull setup into a helper; if it's still huge, the design needs to shrink |

## Red Flags — Stop and Restart from RED

Hearing yourself reach for any of these is the signal, not a reason to continue:

- Writing implementation before the test exists
- A test that passed on the very first run
- Unable to say why a test failed
- "I'll add tests once this is working"
- "Already manually checked it, that's close enough"
- "Tests-after get us the same place"
- "It's fine, I'm honoring the spirit of it"
- "I'll keep the old code as reference while I write tests"
- "Too much time invested to throw this away now"
- "Strict TDD is dogma; I'm being practical"

Every one of these means: discard the code, restart from a failing test.

## Debugging Integration

A bug report is a missing test wearing a different hat. Reproduce it as a failing test, name the falsifiability probe, then run the normal cycle. The passing test is your proof the bug is gone and your guard against it coming back.

Never patch a bug without a test that fails first for that exact reason.
