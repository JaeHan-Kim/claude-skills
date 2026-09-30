---
name: clean-architecture
description: >-
  Use when business logic leaks into frameworks or controllers, or layer boundaries need designing. Triggers: "의존성 규칙", "레이어 아키텍처", "비즈니스 로직이 컨트롤러에", "clean architecture", "ports and adapters".
license: MIT
metadata:
  author: wondelai
  version: "1.0.0"
scenarios:
  - "design a clean architecture for this service"
  - "my business logic is leaking into the web layer"
  - "how do I implement ports and adapters?"
  - "클린 아키텍처 적용해줘"
  - "의존성이 잘못된 방향으로 흘러가고 있어"
  - "비즈니스 로직이 컨트롤러에 너무 많이 들어가 있어"
effort: high
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 의존성 방향 위반과 경계 설계 트레이드오프 분석이 더 정확해집니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER draw the four concentric circles unless the user asks, and never before listing the real import arrows. A diagram drawn first shows the architecture the team wishes it had and hides the one it has.
- ALWAYS cite each dependency violation as `importer → imported` with `file:line`. An unquoted "the domain depends on the framework" cannot be rechecked or fixed.
- ALWAYS decide "business rules testable without a database or server?" by running the use case tests without the framework module and quoting the exit status, not by reading or impression. Self-assessed layering is almost always generous.
- NEVER invent the project's entities or use cases. Mark them `[확인 필요: 엔티티 목록]` — an invented domain produces boundaries around nothing.
- Goal: each violation found has an inversion plan, and the count of outward imports in the inner circles is counted by grep now and the "after" is labelled projected (recount by the same grep only once code changes). Stop at the plan unless the user asks for code; report what stays open.

# Clean Architecture

Keeps business rules ignorant of frameworks, databases, and delivery. It finds where the dependency arrows point the wrong way and inverts them.

**Not for** naming and function size (develop:clean-code) or bounded contexts and domain language (develop:domain-driven-design).

## Process

1. **Read the tree.** List modules or packages and grep their imports; ask nothing the repo answers. Structure not available → ask in one line for the module list.
2. **Find violations.** Use `think-tool`, if available, to trace each import chain from entities outward. Every import from an inner circle to an outer one (ORM, HTTP, SDK types) is one row, quoted.
3. **Test the claim.** Run a use case test with no framework module on the classpath and quote the exit status. Cannot run it → `[확인 필요: 테스트 실행 여부]`.
4. **Plan the inversion.** For each row, name the interface to define in the inner circle and the class to move outward. Load `references/framework.md` for circles, SOLID, and boundary patterns, then the matching file in `references/` (dependency-rule, entities-use-cases, adapters-frameworks, component-principles, solid-principles, boundaries).
5. **Project** the outward imports left if the plan were applied (label it projected; grep again after code changes). Nonzero → list each remainder with its reason.

## Output Template

```
Violations: <n> outward imports (entities <a> · use cases <b> · adapters <c>)
| # | importer → imported | file:line | inversion |
Plan: <interfaces to extract · classes to move>
Remaining after plan (projected): <n> — <reason each, or "none">
Verdict: <n> violations found, <m> planned inversions, tests without framework <command → exit status | [확인 필요]>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Greps imports and quotes each violation | Share the module structure if the repo is not visible |
| Defines the interface contracts at each boundary | Confirm the business rules and entities |
| Projects the remaining violations after the plan | Implement outer-circle classes and wire the composition root |

## Related Skills

- `develop:clean-code` — code-level quality inside each layer
- `develop:domain-driven-design` — domain modelling and bounded contexts
- `develop:architecture-designer` — system-level and deployment decisions
