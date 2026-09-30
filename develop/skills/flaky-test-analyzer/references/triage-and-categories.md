# Flaky test triage, categories, fix quick reference, prevention

Moved out of SKILL.md. Category-specific code: `flaky-fix-patterns.md`.

## Triage: Find the Category First

| Fails When | Category |
|-----------|----------|
| Run repeatedly in isolation | Timing dependency or resource leak |
| Run after specific other tests | Ordering / shared state dependency |
| Run in parallel | Concurrency or shared resource conflict |
| Run on CI but not locally | Environment dependency (clock, timezone, path, env var) |
| Run with real external systems | External dependency (network, DB, third-party API) |
| Passes after a sleep/wait | Timing / async race condition |

## The 5 Flakiness Categories

**1. Timing Dependencies** — Asserts on async work before it completes.
Fix: use `waitFor`/`awaitility`, event-driven signals, or inject a controllable `Clock`. Never use `Thread.sleep`.

**2. Shared State Between Tests** — Tests pollute database, static variables, in-memory caches, or file system.
Fix: reset state in `@BeforeEach`/`@AfterEach`; use `@Transactional` rollback or explicit truncate; prefer instance injection over singletons.

**3. External Dependencies** — Tests call real HTTP APIs, databases, or message queues.
Fix: mock at the boundary (WireMock, Mockito); use Testcontainers for integration tests needing a real DB.

**4. Test Ordering Dependencies** — Test B implicitly relies on state created by Test A.
Fix: self-contained setup per test; run tests in random order (`--randomly-seed=random`).

**5. Concurrency and Parallelism** — Parallel tests share ports, files, or singletons.
Fix: use port 0 (OS-assigned); inject resources so each test gets its own instance.

## Fix Patterns Quick Reference

| Root Cause | Fix |
|-----------|-----|
| Async race condition | Use `waitFor` / `awaitility`; never `Thread.sleep` |
| System clock dependency | Inject `Clock`; use fixed clock in tests |
| Database pollution | `@Transactional` rollback or truncate in `@BeforeEach` |
| Static/singleton state | Reset in `@BeforeEach`/`@AfterEach`; prefer instance injection |
| Real HTTP/DB calls | Mock with WireMock, Mockito, or Testcontainers |
| Ordering dependency | Self-contained setup; run tests in random order |
| Port conflict | Use port 0; never hardcode test ports |
| Timezone sensitivity | Set `TZ=UTC` in CI; use `ZonedDateTime` not `Date` |
| Random data collisions | Use unique test data per run (UUID prefix) |

## Prevention (for the prevention rule in the report)

- Run tests in random order in CI by default
- Quarantine any test that flakes more than 1% of runs
- Never commit a "re-run on failure" workaround without a ticket to fix the root cause
- Fail the build on any `@Disabled` / `@Ignore` without a linked issue

