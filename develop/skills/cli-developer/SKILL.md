---
name: cli-developer
description: >-
  Use when building a command-line tool — subcommands, flags, prompts, progress bars, completions, distribution. Triggers: "build a CLI", "CLI 도구 만들어줘", "커맨드라인 앱", "shell completion".
effort: medium
scenarios:
  - "Build a CLI tool that manages deployment configurations across environments"
  - "I need to create a command-line interface for our internal developer tools"
  - "Help me design a CLI with subcommands, flags, and interactive prompts"
  - "CLI 도구를 만들어줘 — 배포 설정을 관리하는 커맨드라인 앱"
  - "개발자용 내부 CLI 툴 설계를 도와줘"
  - "쉘 자동완성 스크립트를 추가해줘"
compatibility:
  recommended:
    - think-tool
  remote_mcp_note: >-
    think-tool이 있으면 커맨드 계층 구조와 UX 설계를 더 체계적으로 검토할 수 있습니다.
    Claude 설정 → MCP Servers에서 remote SSE 엔드포인트를 추가하세요.
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: devops
  triggers: CLI, command-line, terminal app, argument parsing, shell completion, interactive prompt, progress bar, commander, click, typer, cobra
  role: specialist
  scope: implementation
  output-format: code
---

## Standing Mandates

- **Forbidden reflex:** NEVER rename or re-flag an existing command while "tidying" the CLI. Scripts and CI jobs call those signatures, and a rename breaks them with no compile error.
- ALWAYS take "it works" from running `<cli> --help`, `<cli> --version`, and the test command, and quote their output. Never claim startup time or platform support you did not measure; mark `[확인 필요: 미측정]`.
- NEVER print diagnostics to stdout (stderr only) or require interactive input with no non-interactive fallback. Piped output and CI are where CLIs break.
- NEVER guess the language or framework. Read the repo first; if empty, ask one line (Node / Python / Go).
- Goal: the command tree was confirmed by the user, `--help` and `--version` run with exit 0, and tests pass. Stop after two red rounds and report.

# CLI Developer

Ships a CLI that scripts can rely on.

**Not for** web UIs or REST APIs, or SRE pipeline integration (develop:sre-engineer).

## Process

1. **Analyze UX.** Workflows and command hierarchy; list every command with its expected `--help` output. Use `think-tool`, if available, for the hierarchy. The user confirms the list before code.
2. **Design commands.** Subcommands, flags, arguments, config; consistent flag names; no existing signature broken.
3. **Select framework** from the repo's language (Node: `commander` → `yargs` → `oclif`; Python: `typer` → `click` → `argparse`; Go: `cobra + viper`, `bubbletea` for TUI). Skeleton: `references/quick-start.md`.
4. **Implement**, then run `<cli> --help` and `<cli> --version`; paste the output.
5. **Polish.** Completions, error messages, progress indicators, TTY detection for color, SIGINT handling.
6. **Test.** Smoke tests on the platforms available; measure startup time if a target exists.

Rules: support `--help`/`--version`; validate input early; support interactive and non-interactive modes; use `os.homedir()` / `Path.home()`, not hardcoded paths.

| Topic | Reference |
|-------|-----------|
| Design Patterns | `references/design-patterns.md` |
| Node.js CLIs | `references/node-cli.md` |
| Python CLIs | `references/python-cli.md` |
| Go CLIs | `references/go-cli.md` |
| Go TUI | `references/go-tui.md` |
| UX Patterns | `references/ux-patterns.md` |

## Output Template

```
Commands: <tree, confirmed | not confirmed>
Files: <entry · config · implementation · completions>
Checks: --help <exit> · --version <exit> · tests <exit>
Verdict: <n> commands, <n> with --help verified · tests <green | red | not run>
```

## What Claude Does / What You Do

| Claude | You |
|--------|-----|
| Proposes the command hierarchy and writes the framework code | Confirm the UX matches your users' workflows |
| Runs help, version, and tests and quotes the output | Test on every target platform and verify completions in your shell |
| Flags signature breaks and stdout/stderr misuse | Decide whether a rename ships and run final packaging |

## Related Skills

- `develop:sre-engineer` — CLI tools inside SRE pipelines
- `develop:code-documenter` — documenting commands and flags
