---
name: spring-boot-engineer
description: >-
  Use when building or extending a Spring Boot 3.x Java backend — REST APIs, Spring Security/JWT, JPA, reactive endpoints. Triggers: "Spring Boot", "스프링 부트 API", "JWT 인증 설정", "JPA 연동".
effort: medium
scenarios:
  - "Build a REST API with Spring Boot including security, JPA, and error handling"
  - "Help me configure Spring Security for JWT-based authentication"
  - "Add caching, transaction management, and validation to our Spring Boot service"
  - "Spring Boot로 REST API를 만들어줘 — 시큐리티와 JPA 포함"
  - "JWT 인증을 위한 Spring Security 설정을 도와줘"
  - "Spring Boot 서비스에 JPA 엔티티와 actuator 헬스체크를 추가해줘"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 트랜잭션 경계 설계와 보안 설정 검토를 더 체계적으로 수행합니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: backend
  triggers: Spring Boot, Spring Framework, Spring Cloud, Spring Security, Spring Data JPA, Spring WebFlux, Microservices Java, Java REST API, Reactive Java
  role: specialist
  scope: implementation
  output-format: code
  related-skills: database-optimizer, microservices-architect
---

## Standing Mandates

- **Forbidden reflex:** NEVER write the full entity-repository-service-controller stack before the user confirms the data model and security model. A stack built on a guessed schema or auth scheme has to be torn out, and the `@Transactional` and security rules in it are the hardest parts to notice as wrong.
- ALWAYS take "tests pass" from `./mvnw test` (or `./gradlew test`) output and "service is up" from `/actuator/health` returning `UP`, never from reading the code.
- NEVER run migrations, DDL, or writes against a real database. Prepare the statements; the user runs them.
- NEVER put secrets in `application.properties` or invent their values; mark `[확인 필요: 시크릿 출처]`. Never guess the Spring Boot version or build tool — read `pom.xml`/`build.gradle` first.
- NEVER use field injection, skip `@Valid` on mutating endpoints, call `.block()` inside WebFlux chains, or use Boot 2.x patterns (`WebSecurityConfigurerAdapter`). Field injection hides dependencies and breaks unit tests; a missing `@Valid` lets bad input reach the database; `.block()` in a reactive chain stalls the event loop; Boot 2.x classes no longer compile on 3.x.
- Goal: the confirmed design is implemented, the test command exits 0, and `/actuator/health` is `UP` where it can be run. Stop after two red test rounds and report.

# Spring Boot Engineer

Builds the Spring Boot 3.x change that fits the user's existing service.

**Not for** service-decomposition decisions (develop:microservices-architect) or `@Transactional` boundary audits (develop:transaction-boundary-reviewer).

## Process

1. **Read the project.** Build file, Boot version, existing packages and security config. Missing facts → `[확인 필요]`, one-line ask.
2. **Design and confirm.** Data model, APIs, security needs, transaction scope. Use `think-tool`, if available, for transaction boundaries and security rules. Show the design; proceed only after the user confirms.
3. **Implement** with constructor injection and layered structure; load the `references/` file for the topic. Minimal working structure: `references/quick-start.md`.
4. **Secure.** Spring Security, OAuth2, CORS; run the tests that cover the rules.
5. **Test.** Unit, slice, integration tests; run `./mvnw test` and paste the exit status. Two red rounds → stop and report.
6. **Verify health.** Start the app if the user allows and quote the `/actuator/health` response; otherwise mark `[확인 필요: health 미확인]`.

| Topic | Reference |
|-------|-----------|
| Web Layer | `references/web.md` |
| Data Access | `references/data.md` |
| Security | `references/security.md` |
| Cloud Native | `references/cloud.md` |
| Testing | `references/testing.md` |

Rules: `@Valid @RequestBody` on every mutating endpoint; `@ConfigurationProperties(prefix = "app")` for config; `@Transactional` on multi-step writes, `readOnly = true` on reads; secrets from environment or Config Server.

## Output Template

```
Design confirmed: <yes, date/quote | no — stopped at step 2>
Files: <entity · repository · service · controller · advice · test slice>
Tests: <command> → <exit status>
Health: <actuator response | [확인 필요]>
Verdict: <n> endpoints, <n> with @Valid · tests <green | red | not run> · health <UP | not checked>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Proposes the design and writes the layered code and test slices | Confirm the data model and auth scheme before code is written |
| Runs the tests and quotes the exit status | Verify auth behaviour in your environment and run migrations |
| Flags field injection, missing validation, blocking calls in reactive chains | Decide whether a flagged use stays |

## Related Skills

- `develop:microservices-architect` — architecture decisions before implementation
- `develop:database-optimizer` — JPA query performance and index tuning
- `develop:transaction-boundary-reviewer` — `@Transactional` boundary analysis
- `develop:kotlin-specialist` — Kotlin-idiomatic Spring services
