---
name: domain-driven-design
effort: high
description: >-
  Use when aligning code with business concepts, drawing bounded contexts, or when domain experts and developers disagree on terms. Triggers: "도메인 모델링", "바운디드 컨텍스트", "유비쿼터스 언어", "DDD", "bounded context".
license: MIT
metadata:
  author: wondelai
  version: "1.0.1"
scenarios:
  - "help me model this business domain"
  - "how do I define bounded contexts for this system?"
  - "도메인 모델 설계해줘"
  - "바운디드 컨텍스트 어떻게 나눠야 해?"
  - "도메인 전문가와 개발자 언어가 달라서 문제야"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 바운디드 컨텍스트 경계와 컨텍스트 매핑 트레이드오프를 더 정확하게 따질 수 있습니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER coin a ubiquitous-language term, an invariant, or a context owner the user did not give. A glossary Claude filled in from the description reads as authoritative and the team then codes against words no domain expert ever said.
- ALWAYS mark each unknown as `[확인 필요: ○○]` (term meaning, invariant, owner) and ask for it in one line, not a menu. Claude cannot run the expert conversation; a guessed answer hides that it never happened.
- ALWAYS label each boundary, aggregate, and event `user-given` or `proposed`, with what would overturn it. A proposal the user cannot tell from their own words is accepted by default.
- NEVER rate the model with a score. A 0–10 the author gives their own draft cannot be recounted; report counts.
- Goal: every context, aggregate, and event is labelled and every open fact is a `[확인 필요]`. Stop after two rounds of the user's corrections and report what is still open.

# Domain-Driven Design

Models code around the business domain — language first, then boundaries, then building blocks.

**Not for** layer or dependency rules (develop:clean-architecture), service split or merge calls (develop:service-boundary-validator), or simple CRUD with no business rules.

## Process

1. **Intake.** Take the domain description, code, or notes the user attached; read the repo before asking what it answers. Missing glossary, invariant, or owner → `[확인 필요: ○○]`, one-line ask.
2. **Ubiquitous language.** List only terms quoted from the user's material, each with its source. Technical-only names (`Manager`, `Helper`, `Utils`) are flagged, not renamed by guess.
3. **Bounded contexts.** Where one term changes meaning, propose a boundary and mark it `proposed`. Use `think-tool`, if available, to weigh context-map relationships (ACL, shared kernel, conformist) when two fit.
4. **Building blocks.** Classify each object Entity, Value Object, or Aggregate; state the invariant it protects — from the user, else `[확인 필요: invariant]`.
5. **Events and repositories.** Name events in past tense from the user's process; interface signatures only, no persistence code.
6. **Distill.** Mark core, supporting, generic subdomains as `proposed`; the user picks where effort goes.

The six framework parts with patterns and examples: `references/framework.md`. Per-topic depth: `references/ubiquitous-language.md`, `references/bounded-contexts.md`, `references/building-blocks.md`, `references/domain-events.md`, `references/repositories-factories.md`, `references/strategic-design.md`. Mistake and diagnostic tables: `references/common-mistakes.md`.

## Output Template

```
Contexts: | name | owner | proposed / user-given | overturned if |
Language: | term | context | source quote |
Aggregates: | root | invariant | state transitions |
Events: | past-tense name | publisher | consumers |
Open: <each [확인 필요: ○○], or "none">
Verdict: <n> contexts · <n> aggregates · <n> events · <n> open [확인 필요]
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Quotes terms, proposes boundaries, classifies objects, and labels each | Supply the terms, invariants, and owners Claude marked `[확인 필요]` |
| Names what would overturn each proposed boundary | Validate with domain experts and the product team |
| Writes event names and repository signatures | Decide the contexts and implement in infrastructure |

## Related Skills

- `develop:clean-architecture` — architecture layers and dependency rule
- `develop:event-storming` — workshop technique to discover domain events collaboratively
- `develop:service-boundary-validator` — validate microservice decomposition
- `develop:microservices-architect` — distributed system design
