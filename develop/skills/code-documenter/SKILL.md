---
name: code-documenter
description: >-
  Use when code or an API lacks docs: docstrings/JSDoc, OpenAPI specs, a doc site, tutorials. Triggers: "문서화해줘", "docstring 추가", "API 문서 생성", "add JSDoc", "generate OpenAPI", "write a README".
effort: medium
scenarios:
  - "Our codebase has no documentation and new engineers can't understand it"
  - "Generate API documentation from this undocumented codebase"
  - "Write inline comments and a README for this legacy module"
  - "코드베이스에 문서가 없어서 신규 입사자들이 이해를 못 해"
  - "이 모듈에 대한 API 문서를 생성해줘"
compatibility:
  recommended: []
  optional:
    - code-review-graph
  remote_mcp_note: >-
    code-review-graph가 있으면 문서화 대상인 공개 함수와 엔드포인트를 코드 그래프에서 빠짐없이 찾아 커버리지를 더 정확히 셉니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: quality
  triggers: documentation, docstrings, OpenAPI, Swagger, JSDoc, comments, API docs, tutorials, user guides, doc site, README, changelog
  role: specialist
  scope: implementation
  output-format: code
---

## Standing Mandates

- **Forbidden reflex:** NEVER document what the code is meant to do — document what it does. A docstring written from a function's name promises a return value or exception the body never produces, and readers trust the docstring over the code.
- NEVER invent a parameter meaning, return semantic, or rationale you cannot see in the code. Mark it `[확인 필요: 의도]` and leave the line for the owner.
- ALWAYS take "examples compile" from the validator's output, not from reading them. An untested example is the first thing a reader copies and the first thing that breaks.
- ALWAYS match the repo's existing docstring style; ask only if the repo shows none. Mixed styles make the docs unsearchable.
- Touch only the documentation in scope: no code changes, no reformatting, no rewording of docs that are already accurate.
- Goal: every public function, class and endpoint in scope is documented or listed `[확인 필요]`, and the validators exit 0. Stop after two validate-and-fix rounds and report what still fails.

# Code Documenter

Writes the docs the code already proves: docstrings, JSDoc, OpenAPI specs, doc sites, guides.

**Not for** architecture decisions or ADRs (write:plans) or planning a documentation system (develop:documentation-strategy).

## Process

1. **Discover.** Detect language, framework and existing doc style from the repo. No convention found → Google style (Python) or JSDoc (TypeScript/JS) and say so. Scope not stated → ask in one line.
2. **Analyze.** List undocumented public functions, classes and endpoints with `file:line`. Use `code-review-graph`, if available, to find public symbols and route handlers so none is missed. Count them: that is the baseline.
3. **Document.** Apply one format to every target, from signatures and bodies. Examples: `references/quick-examples.md`; per-language detail in the `references/` file listed below. Intent not visible in code → `[확인 필요: 의도]`. Skip obvious getters and setters.
4. **Build the outputs asked for.** README, guides/tutorials, doc site, API docs — only those requested:
   - README / guides / tutorials: structured markdown with runnable examples (`references/user-guides-tutorials.md`, `references/tutorial-structure.md`).
   - Doc site: site config + content structure + build instructions (`references/doc-site-generators.md`, `references/information-architecture.md`).
   - API docs: OpenAPI spec from route handlers + portal configuration (`references/openapi-advanced.md`, `references/api-portals.md`).
5. **Validate and fix.** Run the checks and paste exit status; fix each failure, re-run, at most two rounds, then list what still fails:
   - Python: `python -m doctest file.py` or `pytest --doctest-modules`
   - TypeScript/JavaScript: `tsc --noEmit`
   - OpenAPI: `npx @redocly/cli lint openapi.yaml`
6. **Report.** Recount documented symbols against the baseline. Flag any file under 70% function coverage and any endpoint under 100%.

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Python Docstrings | `references/python-docstrings.md` | Google, NumPy, Sphinx styles |
| TypeScript JSDoc | `references/typescript-jsdoc.md` | JSDoc patterns, TypeScript |
| FastAPI/Django API | `references/api-docs-fastapi-django.md` | Python API documentation |
| NestJS/Express API | `references/api-docs-nestjs-express.md` | Node.js API documentation |
| Coverage Reports | `references/coverage-reports.md` | Generating documentation reports |
| Doc Site Generators | `references/doc-site-generators.md` | Docusaurus, MkDocs, VitePress config |
| OpenAPI Advanced | `references/openapi-advanced.md` | Reusable components, security schemes |
| Tutorial Structure | `references/tutorial-structure.md` | Progressive learning paths |

## Output Template

```
Baseline: <n> public symbols / endpoints in scope, <m> undocumented
Documented: <files> — style: <Google | JSDoc | other, detected | defaulted>
Outputs: <README | guides/tutorials | doc site config + structure + build steps | OpenAPI spec + portal config> — as requested
Validation: <command> → <exit status>
Coverage: <functions %> · <endpoints %>
Open: <k> × [확인 필요: 의도] — <file:line list>
Verdict: <documented> of <n> symbols documented, <k> open, validators <green | red>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Detects existing conventions and lists undocumented symbols | Confirm scope and format preference |
| Writes docs from signatures and bodies, marks unknown intent | Review for accuracy against real behaviour and fill the markers |
| Drafts OpenAPI from route handlers | Validate request and response examples against the live API |
| Writes the README, guides, doc-site structure and OpenAPI spec + portal config that were asked for | Pick the site generator and hosting; supply product context for tutorials |
| Runs validators, fixes, re-runs (two rounds) and recounts coverage | Decide whether files under the 70% gate get another pass |

## Related Skills

- `develop:documentation-strategy` — plan a documentation system first
- `write:plans` — ADR and design-doc format
- `develop:frontend-developer` — JSDoc alongside React component builds
