---
name: dockerfile-optimizer
description: >-
  Use when someone shares a Dockerfile and needs it improved for build speed, image size, or security. Triggers: "도커 최적화", "이미지 크기", "빌드 시간", "Dockerfile", "docker optimize", "이거 좀 봐줘" (Dockerfile pasted).
effort: medium
scenarios:
  - "optimize this Dockerfile"
  - "why is my Docker image so large?"
  - "make my builds faster"
  - "도커파일 최적화해줘"
  - "이미지 크기 줄이는 방법"
  - "빌드가 너무 느려요"
compatibility:
  recommended: []
  optional: []
---

## Standing Mandates

- **Forbidden reflex:** NEVER apply a base-image swap or drop a security control (non-root user, pinned version, secret handling) to shrink the image without the user's decision; propose it, with the reason. A smaller image on a base the app was never tested on breaks at runtime (glibc vs musl), and a removed control ships unnoticed.
- ALWAYS run all 8 checks and list every finding before changing anything. Fixing the one visible issue first hides the ones that interact with it (layer order vs cache vs multi-stage).
- ALWAYS measure size and build time before and after with `docker image ls` and `docker build`; never estimate them. A claimed "60% smaller" that nobody measured is a guess.
- NEVER assume the registry, target runtime, or base-image constraints. Mark them `[확인 필요: 베이스 이미지 제약]` (or `런타임`, `레지스트리`) and change nothing that depends on them.
- NEVER put a secret in `ENV` or `ARG`, including in the "after" you write; it stays readable in `docker history`.
- Goal: all 8 checks resolved or explicitly left with a reason, and the user's own before/after size and build-time numbers are in the report. One fix pass; a second only for a regression the measurement shows.

# Dockerfile Optimizer

Analyzes a Dockerfile and delivers before/after changes for layer caching, image size, build speed and security.

**Not for** Kubernetes manifests, docker-compose orchestration, or runtime security policy (AppArmor, seccomp); production deployment and health checks (develop:sre-engineer).

## Process

1. **Intake.** Read the Dockerfile and `.dockerignore` from the repo or the paste. Note stack and entrypoint. Missing base-image constraints, registry or runtime → `[확인 필요: …]`; ask at most one line.
2. **Baseline.** Ask the user to run `docker image ls <image>`, `docker build --no-cache .` and a source-only rebuild, and paste the output. No numbers → `[확인 필요: 베이스라인]` and go on without a size claim.
3. **Analyze (pass 1, no edits).** Go through the 8 checks in order: base image, multi-stage, RUN consolidation, `.dockerignore`, non-root user, COPY vs ADD, CMD/ENTRYPOINT form, secrets. Quote the offending line per finding with severity. Bad/Good catalog: `references/eight-checks.md`; per-check antipatterns: `references/antipatterns.md`; ignore file: `references/dockerignore-template.md`.
4. **Fix (pass 2).** Apply fixes as an annotated before/after diff. Any base-image change is proposed with the reason and left for the user's decision.
5. **Measure.** The user re-runs the step 2 commands (plus `docker history <image>` or `dive` for large layers); compare. A regression → one more fix round, then report.

## Output Template

```
Findings: <n> (Critical <a> · High <b> · Medium <c>) across 8 checks
| # | check | Dockerfile:line | finding | fix |
Diff: <annotated before/after>
Measured: image <before → after> · cold build <before → after> · warm build <before → after>
Open: <k> × [확인 필요: …]
Verdict: <resolved> of <n> findings resolved, size <delta | not measured>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Lists all 8-check findings with quoted lines before editing | Provide the Dockerfile, stack and base-image constraints |
| Produces the annotated before/after diff and the `.dockerignore` | Decide on any base-image change |
| Compares the before/after numbers | Run `docker build` and the size and time measurements |
| Flags secrets in layers | Move secrets to BuildKit or runtime injection and rotate exposed ones |

## Related Skills

- `develop:sre-engineer` — production container deployment and health checks
- `develop:chaos-engineer` — resilience testing for containerized services
- `develop:cli-developer` — wrapping container tooling in a CLI
