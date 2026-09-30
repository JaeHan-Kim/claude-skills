---
name: dev-quality-workflow
description: >-
  Use when starting a new feature or system from scratch and wanting a full quality process, architecture through incident readiness. Triggers: "dev quality process", "새 기능 처음부터 제대로", "개발 품질 전체", "full dev cycle".
type: workflow
theme: engineering
effort: high
scenarios:
  - "run the full dev quality workflow"
  - "let's build this feature properly from scratch"
  - "full engineering quality cycle"
  - "dev workflow 전체 돌려줘"
  - "새 기능 처음부터 제대로 해보자"
  - "개발 품질 프로세스 시작"
estimated_time: "1-3 days (full), 1-4 hours per step"
compatibility:
  recommended: []
  optional: []
---

## Standing Mandates

- **Forbidden reflex:** NEVER advance to the next step while the previous step's gate is unmet. A domain model built on an unapproved architecture, or a runbook written for code that was never profiled, is rework that looks like progress.
- ALWAYS quote the sub-skill's own closing verdict line before moving on. The step's author does not grade the step; the skill's verdict line does, and you relay it verbatim.
- NEVER supply a missing prior-step output. Mark it `[확인 필요: Step N 산출물]` and ask in one line, or run that step first.
- NEVER skip a step on your own. "Skip if" is the user's call; record the skip and the reason.
- Goal: every step is passed or skipped-with-reason, tracked as `n of 6`. Stop at the first unmet gate and report it; do not loop a step more than twice.

# Dev Quality Workflow

6-step quality process: architecture → domain → test → performance → docs → incident readiness.

**Not for** a quick bug fix or a single-file change. For one topic, go straight to its skill, e.g. (develop:test-driven-development), and see Related Skills.

## Process

Flow diagram and per-step Input/Output detail: `references/workflow-map.md`.

1. **Architecture Design** (`develop:architecture-designer`). Goal: boundaries, component responsibilities, key decisions. Output: diagram, ADR list, complexity class. Gate: the skill's verdict quoted. Skip if architecture is documented and approved.
2. **Domain-Driven Design** (`develop:domain-driven-design`). Input: Step 1 architecture. Output: domain model, context map, glossary. Gate: verdict quoted. Skip if the team already shares a domain model.
3. **Test-Driven Development** (`develop:test-driven-development`). Input: domain model and acceptance criteria. Output: failing-then-passing test suite. Gate: the failing run and the passing run, both quoted. Skip for an exploratory spike; validate first, then TDD.
4. **Performance Profiling** (`develop:performance-profiling-optimization`). Input: working implementation from Step 3. Output: baseline, hotspot evidence, verdict line. Gate: verdict quoted. Skip if performance is non-critical here.
5. **Documentation Strategy** (`develop:documentation-strategy`). Input: Steps 1–4 outputs. Output: coverage map, one doc written. Gate: verdict quoted. Skip for an internal tool with a single maintainer.
6. **Incident Readiness** (`develop:incident-response-playbook`). Input: architecture and known failure modes. Output: runbook, alert thresholds, severity matrix, escalation path. Gate: verdict quoted. Skip if the feature sits behind a flag with zero external traffic.

State tracking: ask which step the user is at and start there ("DDD부터" → Step 2; "성능만" → Step 4). Earlier steps' outputs the user cannot show are `[확인 필요: Step N 산출물]`.

## Output Template

```
| step | skill | gate (quoted verdict) | status |
Passed: <a> · Skipped: <b> (reason each) · Unmet: <c>
Open: <k> × [확인 필요: …]
Verdict: <n> of 6 steps passed or skipped, stopped at <step | none>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Runs each step's skill and quotes its verdict line | Business context, constraints, and the decision to skip a step |
| Stops at the first unmet gate and names it | Domain-expert validation of the model |
| Scaffolds tests and drafts runbooks | Run the tests and load-test with real traffic patterns |
| Tracks `n of 6` | Supply tribal knowledge and operational context |

## Related Skills

- `develop:architecture-designer` — Step 1
- `develop:domain-driven-design` — Step 2
- `develop:test-driven-development` — Step 3
- `develop:performance-profiling-optimization` — Step 4
- `develop:documentation-strategy` — Step 5
- `develop:incident-response-playbook` — Step 6
- `develop:microservices-architect`, `develop:event-storming`, `develop:clean-architecture` — peers
- `think:brainstorming` — before, for design decisions
- `planning:roadmap-planning` — after, Phase 5 (Communicate Roadmap): stakeholder messaging when shipping
