# Workflow Map and Step Details

Flow diagram and per-step Goal, Input, Output, Skip-if. Moved from SKILL.md.

## Workflow Overview

```
[1] Architecture Design
        ↓
[2] Domain Modeling (DDD)
        ↓
[3] Test-Driven Development
        ↓
[4] Performance Profiling
        ↓
[5] Documentation
        ↓
[6] Incident Readiness
```


## Steps

### Step 1 — Architecture Design
**Skill:** `architecture-designer`
**Goal:** Define system boundaries, component responsibilities, key decisions
**Output:** Architecture diagram, ADR list, complexity classification
**Skip if:** Architecture already documented and approved

> "Step 1 시작" 또는 "architecture 설계해줘"


### Step 2 — Domain-Driven Design
**Skill:** `domain-driven-design`
**Goal:** Model the domain with bounded contexts, aggregates, domain events
**Input:** Architecture from Step 1
**Output:** Domain model, context map, ubiquitous language glossary
**Skip if:** Domain is well-understood and team has shared model

> "Step 2 시작" 또는 "DDD 모델링해줘"


### Step 3 — Test-Driven Development
**Skill:** `test-driven-development`
**Goal:** Write failing tests first, then implement to make them pass
**Input:** Domain model + acceptance criteria
**Output:** Test suite (unit + integration), implementation meeting tests
**Skip if:** Exploratory spike — validate concept first, then TDD

> "Step 3 시작" 또는 "TDD로 개발해줘"


### Step 4 — Performance Profiling & Optimization
**Skill:** `performance-profiling-optimization`
**Goal:** Identify bottlenecks, set SLOs, apply targeted optimizations
**Input:** Working implementation from Step 3
**Output:** Performance baseline, hotspot analysis, optimization plan
**Skip if:** Performance is non-critical for this feature

> "Step 4 시작" 또는 "performance 확인해줘"


### Step 5 — Documentation Strategy
**Skill:** `documentation-strategy`
**Goal:** Plan and write the right docs for the right audience
**Input:** Architecture, domain model, APIs from Steps 1-4
**Output:** Doc taxonomy, architecture overview, runbook, onboarding guide
**Skip if:** Internal tool with a single maintainer

> "Step 5 시작" 또는 "문서화 전략 잡아줘"


### Step 6 — Incident Response Playbook
**Skill:** `incident-response-playbook`
**Goal:** Define runbooks, alert thresholds, on-call procedures before going live
**Input:** System architecture + known failure modes
**Output:** Runbook, alert config, severity matrix, escalation path
**Skip if:** Feature is behind a feature flag with zero external traffic initially

> "Step 6 시작" 또는 "incident playbook 만들어줘"



## When to Use

| Use | Skip |
|-----|------|
| Greenfield feature or system | Quick bug fix |
| Major refactor affecting multiple layers | Iterating on existing working code |
| Onboarding a new technology | Single-file or single-function change |
