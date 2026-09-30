---
name: event-storming
effort: high
description: >-
  Use when starting a new product, untangling a legacy system, or mapping how a business process works, before domain modeling. Triggers: "이벤트 스토밍", "도메인 이벤트 정리", "어디서부터 모델링해야 해", "domain modeling", "event storming".
scenarios:
  - "We're starting a new product and need to model the domain before writing code"
  - "Help me run an event storming session to discover bounded contexts"
  - "새 프로덕트 개발 전에 도메인 모델링을 해야 해"
  - "이벤트 스토밍 워크샵을 진행해줘"
compatibility:
  recommended:
    - think-tool
  optional: []
  remote_mcp_note: >-
    think-tool이 있으면 이벤트 클러스터에서 바운디드 컨텍스트 후보 경계를 더 깊이 따질 수 있습니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER name aggregates or contexts before the events are confirmed by the user. Aggregates drawn on a guessed event list get built into the code, and the first real expert conversation contradicts them.
- ALWAYS take events, commands, and actors from the user's list or source document. Claude alone is one voice in a session that needs domain experts; when only the user is here, ask one line for the event list or a doc to read, and mark what they did not say `[확인 필요: ○○]` as a red hotspot.
- NEVER resolve a hotspot by choosing a side. Two conflicting terms are the finding; record both and who would settle it.
- ALWAYS mark cluster names and context candidates `proposed`; the user confirms with domain experts in real business language.
- Goal: Level 1 ends with a confirmed event list and hotspots counted; Level 2 and 3 run only after the user confirms the previous level. Stop at the level the input supports and report the rest as open.

# Event Storming

Discovers bounded contexts by starting from what happens in the business — events first, structure last.

**Not for** implementation code (develop:microservices-architect, develop:spring-boot-engineer), or a domain already modelled and stable (develop:domain-driven-design).

## Process

### Level 1: Big Picture
Goal: the timeline of domain events and the hotspots.

1. Get the events: from the user's list or a source doc, else ask one line for either. A live workshop (6–10 people, at least two domain experts) is the user's to convene.
2. Enforce past tense: "Order Placed", not "Order is placed"; flag noun events.
3. Cluster the timeline; related events hint at candidate contexts, labelled `proposed`. Use `think-tool`, if available, to test where a cluster's language shifts.
4. Mark hotspots where terms shift or the source is silent (`[확인 필요: ○○]`).
5. Name the clusters only after the user confirms the events.

### Level 2: Process Level
Goal: who triggers what and why.

For each confirmed event:
1. What caused this? → Command.
2. Who issued it? → Actor.
3. Is a rule triggering it? → Policy.
4. What does the actor need to see? → Read Model.
5. Crosses a system boundary → External System.

Colours, naming, reading flow: `references/catalog.md`.

### Level 3: Design Level (per confirmed context)
Goal: aggregates and APIs ready for implementation.

1. Group event/command pairs by the state they change → aggregate candidates (`proposed`).
2. Name each aggregate in the context's language from the user's terms.
3. Mark events that cross contexts as integration events.
4. Per aggregate: invariants, transitions, commands — invariants from the user, else `[확인 필요: invariant]`.
5. Eventually-consistent pairs → Saga or Outbox candidates.

Common mistakes and the facilitation checklist are in `references/catalog.md`.

## Output Template

```
Bounded Context (proposed): <name>
Ubiquitous Language: <terms with source quote>
Commands: <list> · Domain Events: <list>
Integration Events (published): <list>
Aggregates: <name, invariants, transitions>
External Dependencies: <contexts or systems>
Hotspots Remaining: <each open question>
Verdict: <n> events · <n> contexts · <n> hotspots open
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Runs the question sequence per sticky type and flags noun events | Supply the events, or convene domain experts and developers |
| Proposes cluster and aggregate names, labelled `proposed` | Confirm names with domain experts in real business language |
| Records hotspots with both conflicting terms | Resolve hotspots with the actual stakeholders |

## Related Skills

- `develop:microservices-architect` — design service boundaries after bounded contexts are discovered
- `develop:service-boundary-validator` — validate the boundaries against team topology principles
- `develop:domain-driven-design` — deeper DDD concepts for aggregates and context mapping
- `write:plans` (ADR format) — document key decisions that emerge
