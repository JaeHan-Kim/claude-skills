---
name: incident-response-playbook
effort: high
description: >-
  Use when a production issue is active or a playbook is needed: severity triage, mitigation, draft Slack updates, blameless RCA. Triggers on "장애 대응", "인시던트 플레이북", "온콜 런북", "production outage", "post-mortem".
scenarios:
  - "We just had a production outage and need a structured incident response process"
  - "Help me create an on-call runbook for database failures"
  - "Design an incident response playbook for our SRE team"
  - "프로덕션 장애가 발생했는데 대응 프로세스가 없어"
  - "온콜 런북과 인시던트 대응 플레이북을 만들어줘"
compatibility:
  recommended: []
  optional: []
---

## Standing Mandates

- **Forbidden reflex:** NEVER open with a root-cause hunt before severity is declared and a mitigation is named; a past P0 stayed down 40 min while three people read logs.
- Severity first: it sets escalation and update cadence. When in doubt, go one level higher.
- Mitigation (restore service) and investigation (find cause) run apart; neither blocks the other.
- Missing timeline entries, owners, or impact numbers: write `[확인 필요: ○○]`; a gap in the timeline is often the cause, so never fill it.
- Slack and status-page text is draft only; Claude never posts it and calls no Slack send tool.
- Blameless: name systems and missing safeguards, never individuals.

# Incident Response Playbook

Speed matters, clarity matters more, blame solves nothing. I have commanded enough P0s to know the first five minutes decide the next five hours.

Goal: a declared severity, a named mitigation, draft comms, and (after resolve) an RCA with a full timeline and owned action items; stop when the RCA is drafted or the user stops.

**Not for** designing SLOs (develop:sre-engineer), proactive failure testing (develop:chaos-engineer), or slow queries in isolation (develop:database-optimizer).

## Process

Lifecycle: Detect, Triage, Communicate, Mitigate, Resolve, Learn. Each phase has an exit; do not skip one under pressure. Templates are in `references/templates.md`.

1. **Detect** -- Open the incident channel now, even while diagnosing. Sources by reliability: alert, synthetic check, user report, a teammate.
2. **Triage** (target < 5 min for P0/P1) -- What is broken, who is affected, when it started, what changed, blast radius. Exit: severity declared and commander assigned. Unknown answers get `[확인 필요: ○○]`.
3. **Communicate** -- Speak before you know the answer; update every 15-30 min for P0/P1. Slack update: draft only, never posted by Claude; the user sends it.
4. **Mitigate** -- Reduce user impact now (rollback, flag off, scale, shed load, redirect, restore). Mitigation is not the fix; record it as temporary.
5. **Resolve** -- Exit when error rate and latency are at baseline, monitors green, no new alerts.
6. **Learn** -- RCA within 48-72 h for P0/P1: timeline reconstruction first, then root cause, contributing factors, owned action items. If the trigger was a product decision, name it and flag the feature owner; go no further.

Escalate by handoff: DB issues to develop:database-optimizer, CPU/memory to develop:performance-profiling-optimization, observability gaps to develop:sre-engineer, storing the RCA to develop:documentation-strategy.

## Output Template

1. Severity and triage answers
2. Mitigation options ranked fastest first
3. Draft Slack and status updates (draft only)
4. RCA draft in the `references/templates.md` format
5. Verdict line

Recount with `grep -c` on the saved RCA draft (`| HH:MM` rows, `[확인 필요`, `@` owners), not by re-reading the list.

```
Verdict: severity P<n>; N of 6 RCA timeline slots filled, K marked [확인 필요]; action items with owner: M
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Classifies severity and drafts triage steps | Declare severity and open the incident channel |
| Drafts Slack and status updates | Review and send them; keep the 15-30 min cadence |
| Proposes mitigation options | Approve and execute the mitigation |
| Writes the blameless RCA draft | Confirm timeline and root cause; schedule the RCA |

## Related Skills

- `develop:sre-engineer` -- SLOs, alerting, runbook gaps found in the RCA
- `develop:chaos-engineer` -- test failure modes before they happen
- `develop:operations-workflow` -- production readiness around this playbook
- `develop:database-optimizer`, `develop:performance-profiling-optimization`, `develop:documentation-strategy`
