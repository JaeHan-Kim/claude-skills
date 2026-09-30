# Dockerfile Mental Model, 8 Checks, Measuring

Layer model, the 8-check Bad/Good catalog and measuring commands. Moved from SKILL.md unchanged.

## The Mental Model: Layers Are Cache Keys

Docker builds images as a stack of immutable layers. Each instruction (`RUN`, `COPY`, `ADD`) creates a new layer. The build cache invalidates a layer — and every layer after it — the moment its instruction or its inputs change.

**Layer order is your primary optimization lever.** Put instructions that change rarely at the top; put instructions that change often (your application code) at the bottom.

```
# Bad — copies source before installing deps; any code change re-runs npm install
COPY . .
RUN npm ci

# Good — deps cached separately; code changes only rebuild the last two layers
COPY package*.json ./
RUN npm ci
COPY . .
```

## The 8-Check Analysis Framework

Work through these in order during the first pass. Note every finding before making any change.

### 1. Base Image Selection

| Choice | Use When |
|--------|----------|
| `alpine` variant | Small production image; minimal tooling needed at runtime |
| `distroless` (Google) | Maximum security; no shell, no package manager |
| `slim` Debian variant | Need glibc compatibility but not full Debian |
| Full official image | Only in build stages, never in final runtime stage |

Avoid `latest` in production. Pin to a digest or at minimum a minor version: `node:20.11-alpine3.19`.

### 2. Multi-Stage Builds

Multi-stage builds are the single highest-impact optimization available. They let you use a fat builder image with compilers and dev tools, then copy only the final artifact into a minimal runtime image.

```dockerfile
# Stage 1: build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: runtime — only the built output, no node_modules, no source
FROM node:20-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
```

### 3. Layer Count and RUN Consolidation

```dockerfile
# Bad — three layers, apt cache left in layer 1
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# Good — one layer, cache never committed
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
```

### 4. .dockerignore

Without a `.dockerignore`, `COPY . .` sends the entire build context to the Docker daemon — including `node_modules`, `.git`, test fixtures, and local config files. See `references/dockerignore-template.md` for a ready-to-use template.

### 5. Non-Root User

```dockerfile
RUN addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --ingroup appgroup appuser
USER appuser
```

Many official images ship a pre-created non-privileged user (`node`, `www-data`) — use it: `USER node`.

### 6. COPY vs ADD

Use `COPY` unless you specifically need `ADD`'s features (auto-extracting tarballs). `ADD` with URLs bypasses the build cache unpredictably.

### 7. CMD vs ENTRYPOINT

Use exec form (`["executable", "arg"]`), not shell form (`executable arg`). Shell form spawns a shell as PID 1, which does not forward signals correctly.

```dockerfile
# Shell form — PID 1 is /bin/sh, signals not forwarded
CMD node server.js

# Exec form — PID 1 is node, SIGTERM reaches your process
ENTRYPOINT ["node"]
CMD ["server.js"]
```

### 8. Secret Handling

Never put secrets in `ENV` or `ARG` — they are visible in `docker history`. Use BuildKit secrets for build-time, and runtime injection for runtime.

```dockerfile
# Good — secret mounted at build time, never committed to a layer
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) ./fetch-assets.sh
```

## Measuring Impact

After optimizing, measure:
- `docker image ls <image>` — compare sizes before and after
- `docker build --no-cache .` — cold build time
- `docker build .` (after changing only source) — warm build time
- `docker history <image>` — layer breakdown; look for unexpectedly large layers
- `dive <image>` (third-party tool) — interactive layer explorer showing wasted space


## When to Use

| Use | Skip |
|-----|------|
| Dockerfile needs size or speed improvements | Kubernetes manifest tuning |
| Build cache misses are causing slow CI | docker-compose service orchestration |
| Container running as root in production | Runtime container security policy (AppArmor, seccomp) |
| Secrets appearing in image layers | |
