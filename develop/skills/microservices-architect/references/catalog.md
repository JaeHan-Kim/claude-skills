# Architect Catalog

Moved out of SKILL.md. Step 0 table, per-step validations, output fields, reference guide, constraints.

## When to Use / When Not to Use

**Use when:**
- Designing service boundaries for a new system or monolith decomposition
- Restructuring a current distributed topology (validating one boundary or split: `service-boundary-validator`)
- Choosing communication patterns (sync REST/gRPC vs. async events)
- Planning resilience, observability, and deployment strategy

**Do not use when:**
- You need implementation code — use `spring-boot-engineer` for coding
- The team has no CI/CD, no container orchestration, and < 2 independent squads — recommend a modular monolith first

## Process

### Step 0: Should You Use Microservices?

Check prerequisites before domain analysis:

| Prerequisite | Present? |
|---|---|
| Automated CI/CD pipeline per service | |
| Container orchestration (Kubernetes or equivalent) | |
| Distributed tracing (Jaeger, Zipkin, or OpenTelemetry) | |
| Team size ≥ 2 independent squads | |
| Clear ownership boundaries across domains | |

**Outcomes:** (a) Proceed with microservices — most prerequisites met. (b) Modular monolith first — mostly absent. (c) Extract one pilot service — build operational muscle before full decomposition.

### Steps 1–6

1. **Domain Analysis** — Take bounded contexts and service boundaries from develop:domain-driven-design / develop:event-storming rather than redoing them. Validation: each candidate service has a clear public API contract and can be deployed independently; where the contexts call for it, it owns its data.
2. **Communication Design** — Choose sync/async patterns. Validation: long-running or cross-aggregate operations use async messaging; only query/command pairs with sub-100ms SLA use sync calls.
3. **Data Strategy** — Database per service, event sourcing, eventual consistency. Validation: where services are meant to deploy independently, no shared database schema exists between them; a shared schema is acceptable only with a stated reason.
4. **Resilience** — Circuit breakers, retries, timeouts, bulkheads, fallbacks. Validation: where a call crosses a service boundary, it has an explicit timeout, retry budget, and degradation path.
5. **Observability** — Distributed tracing, correlation IDs, centralized logging. Validation: a single request traceable end-to-end by correlation ID.
6. **Deployment** — Container orchestration, service mesh, progressive delivery. Validation: health and readiness probes defined; canary or blue-green strategy documented.

## Output Template

Structure output as an Architecture Decision Record (ADR):

**Context:** System state and scope.

**Decision:** Chosen service boundaries with rationale — why these bounded contexts and not alternatives.

**Consequences:** Trade-offs accepted.

**Service Inventory:**

| Service | Responsibility | Data Owned | Communication | SLA |
|---|---|---|---|---|

**Additionally provide:**
1. Service boundary diagram with bounded contexts
2. Communication patterns (sync/async, protocols)
3. Data ownership and consistency model
4. Resilience patterns per integration point
5. Deployment and infrastructure requirements


## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Service Boundaries | `references/decomposition.md` | Monolith decomposition, bounded contexts |
| Communication | `references/communication.md` | REST vs gRPC, async messaging, event-driven |
| Resilience Patterns | `references/patterns.md` | Circuit breakers, bulkhead, retry, health checks |
| Data Management | `references/data.md` | Database per service, Saga, Event Sourcing, CQRS |
| Observability | `references/observability.md` | Distributed tracing, correlation IDs, metrics |

## Constraints

**MUST DO:**
- Take bounded contexts from `develop:domain-driven-design` / `develop:event-storming`; if none exist, run those first or mark `[확인 필요: contexts]` and proceed provisionally
- Use database per service only where the evidence for that service is quoted
- Circuit breakers on external calls only where the call site is quoted
- Add correlation IDs to all requests
- Use async communication for cross-aggregate operations

**MUST NOT DO:**
- Share a database between services that are meant to deploy independently without a stated reason
- Use synchronous calls for long-running operations
- Create chatty service interfaces (> 3 sync hops in user-facing request path)
- Deploy without observability

