---
name: kotlin-specialist
description: >-
  Use when writing Kotlin and needing idiomatic guidance — coroutines/Flow, KMP, Jetpack Compose, Ktor, DSLs. Triggers: "Kotlin coroutines", "코틀린 코루틴", "자바를 코틀린으로", "suspend function".
effort: medium
scenarios:
  - "Help me write idiomatic Kotlin code using coroutines for async processing"
  - "Convert this Java class to Kotlin and apply Kotlin best practices"
  - "Design a Kotlin DSL for our configuration system"
  - "코틀린으로 코루틴 기반 비동기 처리를 구현해줘"
  - "자바 코드를 코틀린으로 전환하고 관용구를 적용해줘"
  - "Flow 수집이 취소될 때 누수가 나는지 봐줘"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 코루틴 스코프 설계와 취소 전파 전략을 더 체계적으로 검토합니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: language
  triggers: Kotlin, coroutines, Kotlin Multiplatform, KMP, Jetpack Compose, Ktor, Flow, Android Kotlin, suspend function
  role: specialist
  scope: implementation
  output-format: code
  related-skills: test-master
---

## Standing Mandates

- **Forbidden reflex:** NEVER rewrite the user's code into a textbook Kotlin style they did not ask for. Idiom applied over the project's existing conventions produces a diff nobody can review and changes behaviour (nullability, dispatchers, cancellation) silently.
- ALWAYS take "it compiles, lints, and tests pass" from the `detekt`, `ktlint`, and test exit statuses, not from your reading of the code. Coroutine bugs read as correct.
- NEVER use `GlobalScope`, `runBlocking` in production code, or `!!` without a documented contract. Each one leaks work or crashes where the caller cannot see it.
- NEVER guess platform targets, Kotlin/coroutines versions, or the null contract of a value. Read `build.gradle(.kts)` first; if absent, mark `[확인 필요: 타깃/버전]` and ask one line.
- Goal: the change compiles, `detekt`/`ktlint` exit 0, tests pass, and every coroutine scope has a named owner that cancels it. Stop after two fix rounds and report what is red.

# Kotlin Specialist

Ships the idiomatic Kotlin change for the codebase in front of it, not a tutorial.

**Not for** Spring Boot Java backends (develop:spring-boot-engineer) or Android XML layouts (this skill covers Compose).

## Process

1. **Read the build.** Open `build.gradle(.kts)`: platform targets, Kotlin and coroutines versions, existing test libs. Missing → `[확인 필요]`.
2. **Design models.** Sealed classes, data classes, type hierarchies. Use `think-tool`, if available, to settle scope ownership and cancellation propagation before writing code.
3. **Implement.** Coroutines, Flow, extension functions; load the `references/` file for the topic (table below). Name the owner of every scope.
4. **Lint.** Run `detekt` and `ktlint`; paste exit statuses; fix violations.
5. **Test.** `runTest` and Turbine for Flow; run the tests and paste the exit status. Two red rounds → stop and report.

Patterns to apply (sealed `UiState`, structured-concurrency repository, null safety): `references/key-patterns.md`.

| Topic | Reference |
|-------|-----------|
| Coroutines & Flow | `references/coroutines-flow.md` |
| Multiplatform | `references/multiplatform-kmp.md` |
| Android & Compose | `references/android-compose.md` |
| Ktor Server | `references/ktor-server.md` |
| DSL & Idioms | `references/dsl-idioms.md` |

## Output Template

```
Models: <files>
Implementation: <files> — scopes: <scope → owner>
Tests: <file> — <command> → <exit status>
Lint: detekt <exit> · ktlint <exit>
Verdict: <n> scopes with owner of <n> · detekt <exit> · ktlint <exit> · tests <green | red | not run>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Writes coroutine, Flow, and sealed-state code and its tests | Provide domain rules and confirm the state model matches real UI states |
| Runs detekt, ktlint, and tests, and quotes the exit status | Run the tests on every platform target |
| Flags `!!`, `GlobalScope`, `runBlocking`, and mixed platform code in common modules | Decide the null contract and whether a flagged use stays |

## Related Skills

- `develop:spring-boot-engineer` — Kotlin inside a Spring Boot service
- `develop:test-master` — broader test coverage for Kotlin/KMP modules
