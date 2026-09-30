---
name: architecture-designer
effort: high
description: >-
  Use when designing or documenting system architecture — topology, trade-offs, ADRs, database choice — or drawing it as a shareable diagram. Triggers: "아키텍처 설계", "아키텍처 그려줘", "시퀀스 다이어그램", "ADR 써줘", "design this system".
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.2.0"
  domain: api-architecture
  role: expert
  scope: design
  output-format: document
scenarios:
  - "should we use microservices or a monolith?"
  - "write an ADR for this technology choice"
  - "diagram a web request: browser, API, Redis cache, Postgres on a miss"
  - "시스템 아키텍처 설계해줘"
  - "마이크로서비스 vs 모놀리스 어떻게 선택해?"
  - "이 결제 흐름을 시퀀스 다이어그램으로 그려서 공유할 수 있게 해줘"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 두 개 이상의 패턴이 맞을 때 트레이드오프와 뒤집힐 조건을 더 정확하게 따질 수 있습니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER recommend a pattern or technology without naming what would overturn it. A bare "use microservices" or "use Postgres" gets adopted as the answer, and nobody knows which fact, if it changed, should reopen it.
- ALWAYS give every ADR at least one rejected alternative with the reason. An ADR with one option records a habit, not a decision.
- ALWAYS cover non-functional requirements from the user's numbers; a missing target is `[확인 필요: ○○]`, never a plausible figure. Invented scale targets drive over-engineering.
- NEVER hand over a diagram HTML that `node scripts/diagram.mjs check` has not passed. A picture that fails the check has overlapping or dangling edges the reader will misread as design.
- Goal: every NFR is covered or marked `[확인 필요]`, every ADR has a rejected alternative, and any shared diagram passed the check. Review loop: at most 2 rounds, then report what still fails.

# Architecture Designer

Designs system topology and records the decisions — each one labelled as a position with what would overturn it.

**Not for** layer or dependency rules (develop:clean-architecture), domain modelling (develop:domain-driven-design), or implementation (develop:spring-boot-engineer, develop:kotlin-specialist).

## Process

1. **Requirements.** Take functional, non-functional, and constraint requirements from the user or the repo. Each NFR without a number → `[확인 필요: ○○]`, one-line ask.
2. **Patterns.** Match requirements to patterns via `references/architecture-patterns.md`. Use `think-tool`, if available, to weigh trade-offs when two or more fit. Label the pick `proposed` with its overturning condition.
3. **Design.** Write the topology with trade-offs. For a diagram a person will open or share: write the IR (`references/diagram-ir.md`), run `node scripts/diagram.mjs check`, apply every repair it prints, then `render` to one HTML file. You place every node; layout is part of the argument. Inline documents may use Mermaid (example in `references/catalog.md`).
4. **Document.** One ADR per key decision with the rejected alternative (`references/adr-template.md`).
5. **Review.** List the NFRs, ADRs, and risks for the user to confirm. Feedback → return to step 3; after 2 rounds stop and report the unresolved items.

Loaded by topic: `references/system-design.md` (full template), `references/database-selection.md`, `references/nfr-checklist.md`. The earlier reference table, constraints, and Mermaid example: `references/catalog.md`.

## Output Template

```
Requirements: <functional> · NFRs: <covered> of <total> (gaps: [확인 필요: ○○] …)
Diagram: <Mermaid | HTML + .json source> — check: <ok | not run, why>
Decisions: | ADR | position (proposed) | rejected alternative | overturned if |
Risks: | risk | mitigation |
Verdict: <n> decisions · <n> with rejected alternative · <n> NFR gaps · diagram check <ok | n/a>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Drafts topology, diagrams, and ADRs with alternatives and trade-offs | Share requirements, numbers, and constraints |
| Labels each recommendation and names what would overturn it | Make the final technology and topology decision |
| Runs the diagram check and applies its repairs | Validate with stakeholders and confirm operational capacity |

## Related Skills

- `develop:clean-architecture` — internal layer dependencies and dependency rule
- `develop:domain-driven-design` — domain modeling and bounded contexts
- `develop:microservices-architect` — distributed system decomposition
- `write:plans` (ADR format) — writing individual Architecture Decision Records
