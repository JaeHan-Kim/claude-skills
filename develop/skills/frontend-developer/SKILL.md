---
name: frontend-developer
description: >-
  Use when building or fixing UI — React components, layouts, hooks, forms, Tailwind (Next.js App Router default). Triggers: "build a React component", "리액트 컴포넌트", "폼 유효성 검사", "모달 버그".
effort: medium
scenarios:
  - "Build a React dashboard with data fetching, state management, and responsive layout"
  - "Help me fix this UI bug where the modal doesn't close properly on mobile"
  - "Implement a form with validation and error handling in our Next.js app"
  - "React 대시보드를 만들어줘 — 데이터 패칭과 상태 관리 포함"
  - "Next.js 폼 유효성 검사 구현을 도와줘"
  - "모바일에서 모달이 안 닫히는 버그를 고쳐줘"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 Server Component vs Client Component 경계 결정과 접근성 검토를
    더 체계적으로 수행합니다. Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
---

## Standing Mandates

- **Forbidden reflex:** NEVER ship a "Client Component for everything" by sprinkling `'use client'` or `useEffect` fetching to make a UI work. It moves data fetching to the browser, inflates the bundle, and hides the server/client boundary the user has to maintain.
- ALWAYS take "it works" from the test run and the typecheck exit status, not from reading JSX. A smoke test that renders proves rendering, not behaviour: say which.
- NEVER assume the project's stack (Next.js version, router, Tailwind version, state library). Read `package.json` first; the defaults here apply only when the project specifies nothing. Missing design or API shape → `[확인 필요: 디자인/API 응답]`, ask one line.
- NEVER use `any`, array-index `key`, `dangerouslySetInnerHTML` without sanitization, or `<img>` without `alt`. Each one fails silently until a user hits it.
- Goal: the component typechecks, the test command exits 0, and the review checklist in step 6 is recounted by grep. Stop after two red rounds and report.

# Frontend Developer

Ships the UI change in the project's own conventions, not a tutorial.

**Not for** Vue, Svelte, or Angular UIs, or backend APIs (develop:spring-boot-engineer).

## Process

1. **Read the project.** `package.json`, router type, existing components, styling approach. Identify component boundaries and server vs client rendering. Use `think-tool`, if available, for the boundary decision. Show the proposed server/client split and stop; proceed only after the user confirms or changes it.
2. **Define types** for props, state, and API shapes before implementation.
3. **Implement** top-down: layout shell, then data-dependent children. Examples: `references/component-patterns.md`.
4. **Style** with mobile-first breakpoints in the project's styling system.
5. **Extract hooks** for non-trivial effects and derived state.
6. **Review by grep**: no `any`; every `useEffect` with side effects returns cleanup; `alt` on every `<img>`; no array-index `key`; ARIA labels on interactive elements; test file present. Run typecheck and tests; paste exit statuses.

State: server/async data in TanStack Query; shared sync UI state in Zustand; local state in `useState`. Forms: Zod schemas; native form + Server Actions when no client interactivity; React Hook Form for complex client forms. Default to Server Components; `'use client'` only for state, handlers, or browser APIs. Type props with explicit interfaces, not `React.FC`.

## Output Template

```
Rendering model: <server | client> — <why, one line>
Files: <types · component · hook · test>
Checks: typecheck <exit> · tests <exit>
Verdict: <n> review items, <n> pass (grep counts quoted) · tests <green | red | not run>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Writes typed components, hooks, styles, and tests | Provide mockups and API response shapes |
| Proposes the server/client split with a reason | Confirm or override the server/client split, and confirm data-fetching and auth context |
| Runs typecheck and tests and quotes the exit status | Check behaviour in the browser and with a screen reader |

## Related Skills

- `develop:spring-boot-engineer` — the backend APIs this UI consumes
- `develop:code-documenter` — JSDoc for props and hooks
- `develop:test-master` — component testing beyond smoke tests
