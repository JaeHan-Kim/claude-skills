---
name: microservices-architect
effort: high
description: >-
  Use when splitting a monolith or re-cutting existing services — where to cut, sync vs async between the pieces, resilience at each seam. Not for validating one existing split (service-boundary-validator). Triggers: "마이크로서비스 설계", "모놀리스 분해".
scenarios:
  - "Design a microservices architecture for our e-commerce monolith migration"
  - "Our microservices topology is tangled — restructure the communication and data design"
  - "모놀리스를 마이크로서비스로 전환하는 아키텍처를 설계해줘"
  - "서비스 경계와 통신 패턴을 어떻게 나눌지 도와줘"
compatibility:
  recommended:
    - think-tool
  optional: []
  remote_mcp_note: >-
    think-tool이 있으면 분해 여부와 동기/비동기 트레이드오프를 더 깊이 따질 수 있습니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: api-architecture
  triggers: microservices, service mesh, distributed systems, service boundaries, domain-driven design, event sourcing, CQRS, saga pattern, Kubernetes microservices, Istio, distributed tracing
  role: architect
  scope: system-design
  output-format: architecture
  related-skills: architecture-designer
---

## Standing Mandates

- **Forbidden reflex:** NEVER recommend decomposition before the Step 0 prerequisites are answered. Splitting a system whose team has no CI/CD, tracing, or independent squads buys network failures and no independent deploys.
- ALWAYS leave an unanswered Step 0 row as `[확인 필요: ○○]` and ask in one line; a guessed "we have Kubernetes" flips the outcome.
- ALWAYS quote the evidence behind each step's validation, or mark it `[확인 필요: ○○]`. "Validation passed" written by the same pass that designed it is a claim, not a check.
- ALWAYS label the design `proposed` with what would overturn it. Dogma ("database per service", "circuit breakers everywhere") is applied only where the evidence for that call site is quoted.
- Goal: Step 0 outcome stated, every step 1–6 validation quoted or open, ADR closes with a count line. One pass; report open prerequisites rather than looping.

# Microservices Architect

Designs a distributed system only after the prerequisites say it should be one — communication, data, resilience, observability, deployment.

**Not for** validating whether one existing boundary or proposed split is real (develop:service-boundary-validator), whole-system topology or ADRs beyond the service split (develop:architecture-designer), or tuning breakers and timeouts (develop:circuit-breaker-tuner).

Scope: the service split — decomposition, communication, data, and resilience between services.

## Process

0. **Should you?** Answer the five prerequisites (CI/CD per service, orchestration, tracing, two or more independent squads, ownership boundaries) from the user or repo; unanswered → `[확인 필요: ○○]`. Outcome: (a) proceed, (b) modular monolith first, (c) extract one pilot. On (b), stop here and say what would change it.
1. **Domain hand-off.** Take bounded contexts from `develop:domain-driven-design` / `develop:event-storming`; do not redo them. None exist yet → run those first, or mark `[확인 필요: contexts]` and apply DDD to identify bounded context candidates as provisional. Each candidate has an API contract and deploys independently; owns its data where the contexts call for it — quoted or open.
2. **Communication.** Sync vs async per operation; long-running or cross-aggregate work is async. Use `think-tool`, if available, when both fit. Latency budgets come from the user's SLA, else `[확인 필요: SLA]`.
3. **Data.** Ownership and consistency model; no shared schema between independently deployed services unless a reason is stated — quoted or open.
4. **Resilience.** Timeout, retry budget, and degradation path per external call; hand parameter tuning to `develop:circuit-breaker-tuner`.
5. **Observability.** A single request traceable by correlation ID — quoted or open.
6. **Deployment.** Probes and rollout strategy documented — quoted or open.

Step tables, per-step validations, and the constraints: `references/catalog.md`. Topic depth: `references/decomposition.md`, `references/communication.md`, `references/patterns.md`, `references/data.md`, `references/observability.md`.

## Output Template

```
Context: <state and scope> · Step 0 outcome: <a | b | c> (unmet: [확인 필요: ○○] …)
Decision (proposed): <boundaries and why not the alternatives> — overturned if: <fact>
Consequences: <trade-offs accepted>
| Service | Responsibility | Data Owned | Communication | SLA |
Validations: | step | evidence quote | met / open |
Verdict: <n> services · <n> sync hops over 3 · <n> prerequisites unmet · <n> open
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Checks the prerequisites and proposes boundaries and patterns with what would overturn them | Answer the prerequisites and provide team structure and SLAs |
| Quotes evidence for each validation and marks the rest open | Confirm against your real deployment capability |
| Writes the ADR-format document | Make the final architectural decision and implement it |

## Related Skills

- `develop:service-boundary-validator` — validate proposed boundaries for distributed monolith patterns
- `develop:event-storming` — discover bounded contexts before designing services
- `develop:circuit-breaker-tuner` — tune breakers, bulkheads, and timeouts
- `develop:spring-boot-engineer` — implement the services after architecture is defined
- `write:plans` (ADR format) — document the architectural decisions
