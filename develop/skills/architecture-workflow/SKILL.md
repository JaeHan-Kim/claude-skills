---
name: architecture-workflow
effort: high
description: >-
  Use when designing a system from scratch, weighing a monolith-to-MSA move, or needing the end-to-end architecture path from domain discovery to ADRs. Triggers: "아키텍처 전체 프로세스", "처음부터 설계", "system architecture from scratch".
type: workflow
theme: architecture
scenarios:
  - "Design a full architecture for our new e-commerce platform from domain events to ADRs"
  - "We need to evaluate whether to break our monolith into microservices — walk me through the process"
  - "처음부터 아키텍처 전체 프로세스 진행해줘"
  - "모놀리스를 마이크로서비스로 전환할지 평가하고 설계까지 해줘"
  - "새 시스템 도메인 모델링부터 ADR 작성까지 단계별로 가보자"
estimated_time: "1-3 days (full), 2-6 hours per step"
compatibility:
  recommended:
    - think-tool
  optional: []
  remote_mcp_note: >-
    think-tool은 서비스 경계 결정과 아키텍처 트레이드오프를 따지는 3·5단계에서 특히 유효합니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER skip a step because the domain "seems understood". A skip Claude decided is the usual reason boundaries get validated against a model nobody confirmed. Only the user's quoted statement that the artifact exists skips a step.
- ALWAYS run each step through its own skill and carry forward only that step's hand-off artifact. Restating a sub-skill here lets the two copies drift.
- ALWAYS stop after each step and wait for the user's confirmation of its artifact. A chain that runs on unconfirmed output compounds every guess.
- NEVER answer a skip condition from inference. Unknown → `[확인 필요: ○○]`, ask in one line.
- Goal: every step is done, or skipped on the user's quoted word, and the hand-off table recounts. Bound: one pass through 1–7; a step the user sends back is redone at most twice, then reported open.

# Architecture Workflow

Domain discovery → modeling → boundary validation → layering → component design → distribution → documentation, one confirmed hand-off at a time.

**Not for** a single-skill task (develop:architecture-designer) or iterating inside a stable architecture; also `develop:dev-quality-workflow` covers the wider engineering cycle after this one.

## Process

1. **Event storming** — `develop:event-storming`. Hand-off: confirmed event list, context candidates, hotspots. Skip only if the user quotes existing contexts and language.
2. **Domain-driven design** — `develop:domain-driven-design`. Hand-off: context map, glossary, aggregates with invariants. Skip only if a validated model exists.
3. **Service boundary validation** — `develop:service-boundary-validator`. Hand-off: five-test result and split/merge position per boundary. Skip only if the user confirms no decomposition is planned. Use `think-tool`, if available, on contested boundaries.
4. **Clean architecture** — `develop:clean-architecture`. Hand-off: layer structure and interface contracts per service. Skip only if the user says services need at most two layers.
5. **Architecture design** — `develop:architecture-designer`. Hand-off: topology, technology positions with overturning conditions, NFR coverage. Use `think-tool`, if available, when two stacks fit. Skip only if stack and topology are approved.
6. **Microservices** (optional) — `develop:microservices-architect`. Hand-off: service inventory and communication map. Skip if the user stays on a monolith or modular monolith.
7. **ADRs** — `write:plans` (ADR format). Hand-off: one ADR per decision, each with a rejected alternative. Never skipped.

Where the user already is: ask which step, e.g. "도메인은 이미 정리됨" → step 3 once they quote the artifact. Per-step Goal/Input/Output, skip conditions, and the flow diagram: `references/step-catalog.md`.

## Output Template

```
| # | step | skill | status (done / skipped — quote / open) | hand-off artifact |
Open: <each [확인 필요: ○○], or "none">
Verdict: <n> of 7 steps done · <n> skipped on quote · <n> open
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Runs each sub-skill in order and records its hand-off | Confirm each artifact before the next step starts |
| Asks for the fact each skip condition needs | Say what already exists, quoting it, to skip a step |
| Writes the ADRs with alternatives and consequences | Make the final technology and topology decisions and store the ADRs |

## Related Skills

- `develop:dev-quality-workflow` — full engineering quality cycle after architecture is set
- `think:redefine-problem` — early-stage decision framing before step 1
- `develop:spring-boot-engineer` or `develop:kotlin-specialist` — implementation after step 7
