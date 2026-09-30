---
name: documentation-strategy
effort: high
description: >-
  Use when a codebase, API, or team has scattered, stale, or missing docs and needs a coverage map plus the highest-leverage doc written. Triggers: "문서화 전략", "온보딩 문서", "문서가 오래됐어", "documentation strategy", "doc coverage".
scenarios:
  - "Our codebase has no docs and new engineers keep asking the same questions repeatedly"
  - "We have documentation but it's scattered across three wikis and no one knows what's current"
  - "Help me build a documentation strategy for our microservices platform"
  - "신규 엔지니어 온보딩이 너무 오래 걸려, 문서화 전략이 필요해"
  - "문서가 분산되어 있고 오래됐어, 체계를 잡아줘"
compatibility:
  optional:
    - code-review-graph
  remote_mcp_note: >-
    code-review-graph가 있으면 문서 커버리지 지도를 만들 때 공개 모듈과 호출 관계를 실제 코드 그래프에서 확인할 수 있습니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---
## Standing Mandates

- **Forbidden reflex:** NEVER write a doc from what the system probably does to fill a template. An invented behaviour, owner, or date in a runbook gets followed at 2am during an incident and makes it worse — read the code or the user's source, or mark the gap.
- ALWAYS audit existing docs before recommending new ones. Redundant docs split the truth in two; the stale copy wins when nobody knows which is current.
- ALWAYS name an audience and a maintenance owner for every doc in the map. A doc without an owner is stale within two quarters.
- NEVER invent an owner, review date, or system fact. Mark it `[확인 필요: 담당자]`, `[확인 필요: 날짜]` or `[확인 필요: 동작]` and leave the field open.
- NEVER recommend a doc without how it stays current (PR-template line, `last_reviewed`, link check).
- Goal: a coverage map with every gap counted, then the top 1 gap written to its template and reviewed by someone outside the author's head. Stop there; at most one doc per run, the rest stay in the map.

# Documentation Strategy

Good documentation answers the right question for the right person at the right time. Wrong documentation misleads with false confidence.

**Not for** inline docstrings or API specs (develop:code-documenter), ADR or design-doc prose (write:plans), or architecture diagrams (develop:architecture-designer).

## Process

1. **Intake.** Read the repo (`README`, `docs/`, runbooks, `CODEOWNERS`) and the wiki links the user gave before asking anything. If no docs location is named and the repo shows none, ask in one line where docs live today.
2. **Audit.** List every existing doc with type, audience, owner and last-reviewed date. Use `code-review-graph`, if available, to list public modules and services with no doc pointing at them. Unknown owner or date → `[확인 필요: 담당자]` / `[확인 필요: 날짜]`. Load `references/strategy-catalog.md` for the type taxonomy, audience questions and freshness rules.
3. **Map gaps.** One row per gap: doc type, audience, trigger (most-asked question, last incident, newest service), owner, update cadence. Count the rows.
4. **Pick one.** Rank by pain and show why the top gap wins. The user confirms or overrides the pick.
5. **Write.** Draft that one doc to its template in `references/templates.md`, from the code and sources you read. Anything you could not read stays `[확인 필요: …]`.
6. **Keep it fresh.** Attach the upkeep mechanism to the doc (owner, `last_reviewed`, PR-template line, index link). A reviewer who matches the audience and is not the author reads it before it merges.

## Output Template

```
Docs found: <n> (current <a> · stale <b> · unknown <c>)
| # | type | audience | owner | last reviewed | gap / action |
Gaps: <n>
Written: <doc, path> — open markers: <k>
Upkeep: <how it stays current>
Verdict: <n> gaps mapped, <1|0> written, <k> [확인 필요] open
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Audits existing docs and marks unknown owners and dates | Point to where current docs live and confirm the owners |
| Maps gaps and ranks the top one with reasons | Pick or override the doc type to start with |
| Drafts the doc from code and sources, markers left open | Fill the markers from what only you know |
| Attaches the upkeep mechanism | Get a reviewer who matches the target audience, then merge |

## Related Skills

- `develop:code-documenter` — inline docs, OpenAPI, doc sites
- `develop:architecture-designer` — system design to document
- `develop:incident-response-playbook` — RCA and runbooks to store
- `write:plans` — ADR and design-doc format
