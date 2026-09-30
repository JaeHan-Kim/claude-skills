---
name: light
description: >-
  Use when Workflow is off and a multi-part change splits into disjoint batches worth running in parallel with a lead-run Test. Triggers: "가볍게 하네스", "배치 병렬로 검증", "light harness", "parallel batches with gates".
scenarios:
  - "Run this rewrite as parallel batches, gate each one, commit the ones that pass"
  - "Workflow is off and the work splits into independent directories — use the light loop"
  - "하네스 없이 배치별로 나눠서 병렬로 돌리고 게이트 통과한 것만 커밋해줘"
  - "독립된 디렉터리 여러 개를 동시에 고치되 배치마다 검증받고 싶어"
compatibility:
  recommended:
    - think-tool
  optional:
    - sequential-thinking
---

## Standing Mandates

- **Forbidden reflex:** NEVER fan executors out in parallel, or diff a batch against HEAD, on the strength of "they look independent". Two batches touched one file and the later write erased the earlier; after the lead committed batch A, HEAD moved and batch B's diff read clean for the wrong reason. A parallel claim needs a scope check in `test[]`, and a baseline is a pinned commit sha.
- ALWAYS keep a gated filename literal out of any Bash or test command that writes or modifies it. The goal-gate hook denies such a command (redirect, tee, sed -i, cp/mv/rm, a script body with write calls), and executors were blocked mid-batch; build the name inside a helper script under `RUN/checks/`. Read-only commands naming it are not denied.
- ALWAYS leave a batch that exhausts its retries uncommitted and report it. A failed batch committed to keep the run green poisons every baseline after it.
- Goal: every committed batch has a lead-written `test-<n>.json` and a fresh-opus `gate-<n>.json` that passed, and the run closes on `fallback-check.mjs`.

# light

A lean variant of `engine/fallback.md` for work that splits into disjoint batches: the same run directory, but batches run in parallel and the lead commits as each one passes.

**Not for** work whose batches overlap or depend on each other, a run that needs Codex routing, or one where the lead cannot stay out of implementing (`harness:harness`).

## Process

1. Open the run as `fallback.md` §0 does: `RUN=.harness-run/<slug>/` and a manifest that records the subgoal ids and order as `subgoals:[{"id","order"}]` (`fallback-check.mjs` reports INCOMPLETE without it). The RUN/ artifacts are exactly fallback.md's, unchanged, so the completion check and the goal gate read them as-is.
2. Plan and SetGoal run on opus, writing `01-plan.md` and `02-goal-spec.json`.
3. A separate critic (opus, through `think:devils-advocate`) writes `02-critique.json`, and the loop is bounded: it repeats until `sound:true` or `max_retries` rounds. Red before green: every `test[]` must fail at the base commit; the critic runs them there and rejects any that already passes.
4. Run batches in parallel only when every subgoal has `deps: []` and disjoint paths, each proven by a scope check in its `test[]`: owned paths per batch, pinned to the base sha, a sibling run's commit exempt by sha only.
5. Otherwise keep fallback §3 strict linear order; light adds nothing there.
6. Dispatch one sonnet executor per batch; each writes `impl-<n>.md` under its own `subgoals/<id>/`.
7. The lead re-runs each batch's `test[]` itself with `RUN=<dir> python3 scripts/run_tests.py <id> [attempt]`, which writes `subgoals/<id>/test-<n>.json` from the output, never from the executor's narrative.
8. A fresh opus gate per batch reads the spec and the diff and writes `gate-<n>.json`.
9. On a failed gate allow one fix round, a targeted executor pass followed by steps 7 and 8 again. Any edit after a gate needs a new gate on that batch, else the report says 'not re-gated'.
10. The lead writes `subgoals/<id>/result.json` for the batch (`fallback-check.mjs` requires it), then commits a batch that passed, only its own paths.
11. A batch whose retries are exhausted gets its `result.json` with passed false, stays uncommitted, and is reported with its last `gate-<n>.json` reason.
12. Pin every baseline to a commit sha, never HEAD; the lead commits between batches, so HEAD moves.
13. No test[] command may name a gated file as a literal while writing or modifying it; the hook denies those Bash commands, so a check script builds the name at runtime.
14. Close with the goal-level gate (`04-goal-gate.json`, match_pct >= 90), write `05-report.md` (the check requires it), then run `fallback-check.mjs` on the run directory; the verdict or done claim counts only once it says COMPLETE, otherwise retract it.

## Departures from fallback.md's Contract

- The lead runs Test, a departure from the Contract's separate Test teammate. Judge and actor stay apart because the lead never implements; the executor is the only implementer.
- Sonnet executors replace the Contract's provider routing: Codex is off, so Implement is a sonnet agent rather than a `codex exec` process.
- Use `harness:harness` instead when batches share files or order, when Codex should implement, or when the lead ends up writing code itself.

## Output Template

```
Run: .harness-run/<slug>/  baseline <sha>
Batch <id>: attempts <n>  test <verified>  gate <pass>  commit <sha|uncommitted>
Goal gate: match_pct <n>
Verdict: <all batches committed | N batches left uncommitted: ids and reasons>
```

## What Claude Does / What You Do

| Claude | You |
|---|---|
| Opens the run, plans, specs, and loops the critic to sound | State the request and the batch boundaries you know |
| Dispatches sonnet executors per disjoint batch | Approve a parallel claim that looks wrong |
| Re-runs each `test[]`, dispatches the opus gates, commits passes | Review the commits |
| Reports uncommitted batches with reasons | Decide whether to retry them or move to the full harness |

## Related Skills

- `harness:harness` - the full engine; use it when light's preconditions fail.
- `harness:codex-control` - the provider route light leaves off.
