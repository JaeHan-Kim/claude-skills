---
name: service-boundary-validator
effort: high
description: >-
  Use when deciding whether to split or merge a service, when services seem too coupled to deploy independently, or when validating a proposed boundary. Triggers: "서비스 분리", "서비스 경계 검토", "분산 모놀리스", "split this service".
scenarios:
  - "Should this feature be a new microservice or stay in the existing service?"
  - "Validate whether our proposed service split makes sense or creates too much coupling"
  - "이 기능을 새 서비스로 분리해야 할지 기존 서비스에 넣어야 할지 모르겠어"
  - "서비스 경계가 맞게 나뉘어져 있는지 검토해줘"
compatibility:
  recommended:
    - code-review-graph
  optional: []
  remote_mcp_note: >-
    code-review-graph가 있으면 서비스 간 호출·import 관계와 영향 범위를 코드에서 직접 뽑아 커플링 근거로 인용할 수 있습니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER issue a split or merge recommendation without data-ownership evidence quoted from the code or the user's table. A boundary drawn from the service names alone splits a shared database in two, and the team ships a distributed monolith.
- ALWAYS take the verdict from the five boundary tests, each passed or failed with a quoted fact. A narrative "looks coupled" cannot be recounted.
- NEVER fill a cell Claude cannot see (owner team, tables written, call sites). Mark it `[확인 필요: ○○]` and ask in one line; a guessed owner flips a test.
- ALWAYS say the recommendation is a position and what fact would overturn it. The split or merge is the user's call.
- Goal: all five tests carry a quoted pass, fail, or `[확인 필요]`, and the verdict line recounts. One evidence pass; if a test still has no fact, report it open rather than loop.

# Service Boundary Validator

Tests whether a service boundary holds — by evidence, not by how the diagram looks.

**Not for** designing boundaries from scratch (develop:event-storming); hand the design step to develop:microservices-architect.

## Process

1. **Coupling.** Map synchronous call chains, shared databases, and bidirectional dependencies. If `code-review-graph` is available, use its graph queries (callers, imports, impact radius) on the named services and quote the edges; otherwise ask for the dependency diagram in one line. Hops over 3 in a user-facing path, any bidirectional pair, any shared schema is a red flag.
2. **Data ownership.** For each entity: who creates, reads, updates, deletes. A writer that is not the creator is a violation. Unseen → `[확인 필요: ○○]`.
3. **Team alignment.** One owning team per service; apply the cognitive-load question. The user states team structure.
4. **Five tests.** Score each test in `references/boundary-catalog.md` pass / fail / `[확인 필요]` with the quoted fact.
5. **Recommendation.** Merge, split, convert to async, or fix ownership — labelled `proposed`, with the overturning fact. Split rules and red-flag fixes are in `references/boundary-catalog.md`.

## Output Template

```
Service: <name> · owner: <team | [확인 필요: 팀]>
Evidence: | entity | owner | other writers | quote / source |
Red flags: <each with quote, or "none">
Tests: | # | test | pass / fail / [확인 필요] | fact |
Recommendation (proposed): <action> — overturned if: <fact>
Verdict: <n> of 5 tests failed · <n> red flags · <n> [확인 필요]
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Pulls call and data evidence, runs the five tests, quotes each fact | Provide the dependency diagram, table access, and team structure Claude cannot see |
| Proposes merge / split / async / ownership fix and what would overturn it | Make the final split or merge decision |
| Marks every unseen cell `[확인 필요]` | Fill those cells from your codebase |

## Related Skills

- `develop:microservices-architect` — design new service boundaries after validation
- `develop:event-storming` — discover bounded contexts to inform boundary decisions
- `develop:transaction-boundary-reviewer` — fix cross-service transaction anti-patterns
- `write:plans` (ADR format) — document the split or merge decision
