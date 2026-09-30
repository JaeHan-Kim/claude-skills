# Incident Templates

All Slack and status-page text below is a draft for the user to send. Claude never posts.

## Severity

| Severity | Definition | Response | Example |
|----------|-----------|----------|---------|
| P0 | Full service down; all users; revenue/data at risk | Immediate page | Checkout API 100% errors |
| P1 | Major feature broken; significant subset | < 15 min | Payments failing for 30% |
| P2 | Degraded or partial failure | < 1 hour | Search latency 10x |
| P3 | Minor; workaround exists | Next business day | Chart missing for 5% |

Escalate up, not down.

## Internal Slack Update (draft)

```
[P0] <Service> - <Brief description>
Status: Investigating / Identified / Mitigating / Resolved
Impact: <Who is affected and how>
Start time: <HH:MM UTC>
Last update: <HH:MM UTC>
IC: @<incident-commander>
Bridge: <link to war room>
Next update: <HH:MM UTC>
```

## Status Page Update (draft)

```
Investigating: We are aware of an issue affecting <service/feature>.
Our team is actively investigating. We will provide an update by <time>.

Identified: We have identified the cause of the issue affecting <service/feature>.
We are working on a fix and expect resolution by <time>.

Resolved: The issue affecting <service/feature> has been resolved as of <time>.
All systems are operating normally. An RCA will be published within 48 hours.
```

Never say publicly: internal system names, architecture-revealing errors, unconfirmed cause.

## Mitigation Options (fastest to slowest)

| Action | When | Risk |
|--------|------|------|
| Rollback last deployment | Started after deploy | Low if clean |
| Disable feature flag | Feature-specific | Low |
| Scale out (increase replica count) | Overload | Medium (cost) |
| Circuit breaker / shed load | Cascading failure | Medium |
| Redirect to healthy region | Regional failure | Medium |
| Restore from backup | Data loss/corruption | High, validate |

## Resolve Exit Criteria

- [ ] Error rate and latency back to baseline
- [ ] All monitors green, no new alerts
- [ ] Affected users notified if required
- [ ] Incident channel closed

## Incident Commander Checklist

- [ ] Severity declared
- [ ] Channel opened
- [ ] Responders assigned (IC, tech lead, comms)
- [ ] First communication drafted and sent by the user
- [ ] Mitigation identified and executing
- [ ] 15-30 min cadence set
- [ ] Resolution confirmed on all metrics
- [ ] RCA scheduled

## RCA Template

```markdown
## Incident RCA: <Title>

**Date**: YYYY-MM-DD
**Duration**: X hours Y minutes
**Severity**: P0 / P1 / P2
**Services Affected**: <list>
**Author(s)**: <names>
**Status**: Draft / Final

### Summary
One paragraph. What happened, what was the user impact, how was it resolved.

### Timeline
| Time (UTC) | Event |
|------------|-------|
| HH:MM | Alert fired / issue first detected |
| HH:MM | On-call paged |
| HH:MM | Triage complete; P0 declared |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Incident resolved |

### Root Cause
Specific, technical explanation. Not "human error" - explain what made the error possible.

### Contributing Factors
- Factor 1 (e.g., no alerting on X metric)
- Factor 2 (e.g., runbook for this scenario was missing)
- Factor 3 (e.g., deploy pipeline did not catch Y in staging)

### What Went Well
- ...

### Action Items
| Item | Owner | Due Date | Priority |
|------|-------|----------|----------|
| Add alert for X | @person | YYYY-MM-DD | High |
| Update runbook for Y scenario | @person | YYYY-MM-DD | Medium |
| Add canary deploy for Z service | @person | YYYY-MM-DD | High |
```

## When Root Cause Traces to a Product Decision

If the trigger was a feature behaving as designed (a rollout hitting an untested segment, a failed launch assumption), action items will not stop recurrence. Add one RCA line: `Product decision to revisit: [decision] - flag to [feature owner] for the next planning cycle.` This skill stops at naming the decision; iterate-vs-pivot is a product-side call.

## Blameless Reframe

Document what systems failed and what made failure possible. Avoid "engineer forgot to". Write "The deploy pipeline had no canary stage that would have caught this", not "Alice pushed bad code."
