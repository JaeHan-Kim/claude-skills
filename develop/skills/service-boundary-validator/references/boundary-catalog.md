# Boundary Catalog

Moved out of SKILL.md. Tests, red flags, split rules and the per-service record.

## The 5 Tests for a Well-Placed Boundary

A service boundary is correct only if all five hold:

1. The service can be deployed independently without coordinating with other services
2. A single team can own it without ongoing negotiation with other teams
3. Its data is owned exclusively — no other service writes to its database tables
4. Its domain language is consistent — terms do not shift meaning at the boundary
5. Failure of this service degrades, but does not break, other services

If any fails, the boundary is suspect.

## Red Flags: Distributed Monolith Patterns

### Shared Database

Services A and B both write to the same schema, or A reads B's tables directly via SQL. The database becomes the integration point — schema changes require coordinating both services.

**Fix:** Each service owns its data exclusively. Other services access it only through the owning service's API.

### Chatty APIs (Temporal Coupling)

To complete one user-facing operation, Service A makes 5+ synchronous calls to B, C, D in sequence.

**Threshold:** More than 3 synchronous hops in a user-facing request path is a warning sign.

**Fix options:** Merge if always called together; use async events for non-blocking workflows; BFF/API composition at the edge.

### Bidirectional Dependencies

Service A calls B, and B also calls A. This means deployment order is undefined and neither service is the source of truth.

**Fix:** Identify the natural authority direction. Introduce an event or callback pattern if the consumer needs to communicate back.

### Deployment Coupling

All services must be deployed simultaneously. This reveals implicit shared contracts that change together — no deployment independence exists.

**Diagnosis question:** "Can we deploy Service A on Monday and Service B the following Friday?"

## Split Decision Framework

```
Should service X be split into A and B?

Yes, split if:
  - A and B are owned by different teams
  - A and B have different deployment frequencies
  - A and B have different scaling requirements
  - A and B have clearly distinct ubiquitous language

No, keep together if:
  - A and B always change together
  - A and B are always called together in every operation
  - A and B are owned by the same team with no plans to split
  - Splitting would create a shared database problem
  - The split introduces a distributed transaction requirement
```

## Data Ownership Analysis

```
For each entity E:
  1. Which service creates E? → That service owns E.
  2. Which services read E? → They call the owning service's API or receive events.
  3. Which services update E? → Any service other than the owner is a violation.
  4. Which services delete E? → Same — only the owner deletes.
```

## Quick Checklist

- [ ] Each service has exactly one owning team
- [ ] No service reads another service's database directly
- [ ] Synchronous call chains are ≤ 3 hops for user-facing requests
- [ ] No bidirectional synchronous dependencies
- [ ] Services can be deployed independently
- [ ] Each service's ubiquitous language is internally consistent
- [ ] Data ownership is unambiguous for every entity
- [ ] Cross-service writes use events + outbox, not shared transactions


## Per-service record


```
Service: [Name]
Owner Team: [Team name]
Data Owned: [List of tables/entities]
Data Read from Others: [Entity → owning service, access method]
Synchronous Dependencies: [Service → purpose → can it be made async?]
Events Published: [Event name → consumers]
Events Consumed: [Event name → publisher]

Red Flags Found:
- [Specific coupling issue]

Recommendation:

## Earlier scope

## When to Use / When Not to Use

**Use when:**
- Evaluating whether services can actually deploy independently
- Suspecting a distributed monolith (coupled services with shared database or chatty sync calls)
- Deciding whether to split or merge services
- Auditing data ownership before a migration

**Do not use when:**
- Designing new boundaries from scratch — run `event-storming` first, then use `microservices-architect`
