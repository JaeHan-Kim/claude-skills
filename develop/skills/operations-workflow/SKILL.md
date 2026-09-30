---
name: operations-workflow
effort: high
description: >-
  Use when preparing a service for production, hardening a flaky system, or building lasting ops after an incident. Triggers on "production readiness review", "going to prod", "system hardening", "운영 준비", "프로덕션 출시 점검".
type: workflow
theme: operations
scenarios:
  - "Run a full production readiness review before we launch next week"
  - "New microservice going to prod — walk me through the full ops setup"
  - "System has been flaky in production, help me harden it end-to-end"
  - "프로덕션 출시 전 운영 준비 전체 점검해줘"
  - "새 서비스 처음 배포하는데 운영 셋업 단계별로 가보자"
  - "장애 반복되는 서비스 안정화 프로세스 전체 돌려줘"
estimated_time: "4-16 hours (full), 1-3 hours per step"
compatibility:
  recommended: []
  optional: []
---

## Standing Mandates

- **Forbidden reflex:** NEVER mark a step done without evidence (output artifact or user-reported result); a green checklist with no evidence is how unready services launch.
- NEVER inject faults, or hand a fault-injection command to be run, at Step 5 without the user's explicit go; the injection is the user's action on their environment.
- Missing SLO, latency, or dependency facts: write `[확인 필요: ○○]` and carry the gap forward; never invent them so a step can close.
- Run steps in order; Step 5 needs Step 4 deployed, or it tests nothing.

# Operations Workflow

I have launched services that were "ready" on paper. This walks build, observe, harden, respond, and each step closes only on evidence.

Goal: each of the 6 steps ends as passed (with evidence), skipped (with the stated skip reason), or open (with a `[확인 필요]` gap). Stop after Step 6 or when the user stops.

**Not for** an active incident (develop:incident-response-playbook), or a single-step need (run that skill directly).

## Process

Phases: BUILD = Step 1, OBSERVE = Steps 2-3, HARDEN = Steps 4-5, RESPOND = Step 6; the Use/Skip table and diagram are in `references/phases.md`. Ask one line where the user is if unclear ("SLO 이미 있어" goes to Step 3, "서킷 브레이커 됐어" to Step 5); apply each Skip rule automatically.

1. **Container image** -- `develop:dockerfile-optimizer`. Input: Dockerfile, runtime. Output: annotated diff, size delta, security findings. Skip: not containerized.
2. **SLO and observability** -- `develop:sre-engineer`. Input: architecture, traffic, reliability needs. Output: SLOs, alert rules, error budget policy, runbook stubs. Skip: SLOs approved and alerting active.
3. **Performance baseline** -- `develop:performance-profiling-optimization`. Input: running service with P50/P95/P99. Output: problem statement, profiler evidence, before/after. Skip: performance non-critical and P99 within SLO headroom.
4. **Circuit breakers** -- `develop:circuit-breaker-tuner`. Input: downstream list, latency, recovery times. Output: config, fallbacks, bulkhead, alerts. Skip: no downstream dependencies.
5. **Chaos experiments** -- `develop:chaos-engineer`. Input: Step 4 config deployed, Step 2 monitoring active. Output: experiment design, scripts, learning summary. Design only; the user gives the go and runs it. Skip: no monitoring stack.
6. **Incident playbook** -- `develop:incident-response-playbook`. Input: failure modes from Steps 4-5, SLO thresholds from Step 2. Output: severity matrix, draft Slack templates, runbook, RCA template. Skip: runbooks already cover this service.

Start a step by invoking its skill; the user can say "Step N 시작".

## Output Template

```
Step | Skill | Status (passed / skipped / open) | Evidence or skip reason
1..6 | ...   | ...                              | ...
Open gaps: [확인 필요: ...] list
Verdict: N of 6 steps passed with evidence; K skipped; M open
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Runs each step's skill and records the evidence | Provide inputs and confirm results |
| Drafts SLOs, alert YAML, breaker config | Confirm SLOs reflect real users; test under load |
| Designs chaos experiments with rollback | Give the explicit go, run it, verify rollback |
| Drafts runbook, severity matrix, RCA structure | Add environment-specific operational context |

## Related Skills

- `develop:dev-quality-workflow` -- greenfield quality cycle, overlaps at Step 6
- `develop:architecture-designer` -- system boundaries before hardening
- `develop:dockerfile-optimizer`, `develop:sre-engineer`, `develop:performance-profiling-optimization`
- `develop:circuit-breaker-tuner`, `develop:chaos-engineer`, `develop:incident-response-playbook`
