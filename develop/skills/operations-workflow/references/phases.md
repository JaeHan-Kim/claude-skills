# Phases and When to Use

Restored from the pre-rewrite skill. The Process in the skill file stays the authority for steps.

## When to Use / Skip

| Use | Skip |
|-----|------|
| Pre-launch production readiness review | Active incident in progress: use incident-response-playbook directly |
| New service going to prod for the first time | Single-step need: run the individual skill directly |
| System showing recurring production issues | Quick config tweak with no systemic gaps |

## Workflow Overview

```
Phase 1: BUILD
  [1] dockerfile-optimizer      ← skip for non-container deployments
        |
        v
Phase 2: OBSERVE
  [2] sre-engineer              ← SLOs, error budgets, golden signals
        |
  [3] performance-profiling-optimization  ← baseline, bottlenecks, fix
        |
        v
Phase 3: HARDEN
  [4] circuit-breaker-tuner     ← downstream resilience, fallbacks
        |
  [5] chaos-engineer            ← run AFTER Step 4 is configured
        |
        v
Phase 4: RESPOND
  [6] incident-response-playbook  ← runbooks, severity matrix, RCA
```

## Step Detail (goal and output)

| Step | Goal | Output |
|------|------|--------|
| 1 | Minimize image size, speed CI cache, harden container security | Annotated before/after diff, size delta, security findings (Dockerfile 8-check analysis) |
| 2 | SLIs/SLOs, golden-signal dashboards, multi-window burn-rate alerts | SLO definitions, Prometheus alert rules, error budget policy, runbook stubs |
| 3 | Latency/resource baseline, bottlenecks, fixes verified with data | Problem statement, profiler evidence (flame graph), before/after |
| 4 | Stop cascading failures from slow or failing downstreams | Resilience4j YAML (or equivalent), fallbacks, bulkhead, state-change alerts |
| 5 | Prove breakers, fallbacks and SLO alerting hold under real failure | Experiment design (hypothesis, blast radius, rollback), injection scripts, learning summary |
| 6 | Severity classification, runbooks, escalation, RCA template pre-launch | Severity matrix (P0-P3), Slack templates, on-call runbook, RCA template |

Step 4 skips when calls are all idempotent fire-and-forget. Step 5 runs only after Step 4 is deployed and verified. Step 6's RCA flags product-decision root causes to the feature owner (see incident-response-playbook, "When Root Cause Traces to a Product Decision").
