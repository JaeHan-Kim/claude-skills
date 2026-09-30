# CLI Quick Start and Constraints (moved from SKILL.md)

## Quick-Start Example (Node.js / commander)

```js
#!/usr/bin/env node
const { program } = require('commander');

program
  .name('mytool')
  .description('Example CLI')
  .version('1.0.0');

program
  .command('greet <name>')
  .description('Greet a user')
  .option('-l, --loud', 'uppercase the greeting')
  .action((name, opts) => {
    const msg = `Hello, ${name}!`;
    console.log(opts.loud ? msg.toUpperCase() : msg);
  });

program.parse();
```

For Python (click/typer) and Go (cobra) examples, see `references/python-cli.md` and `references/go-cli.md`.

## Constraints

**MUST DO:**
- Keep startup time under 50ms
- Support `--help` and `--version` flags
- Use consistent flag naming conventions
- Handle SIGINT (Ctrl+C) gracefully
- Validate user input early
- Detect TTY before applying color output
- Support both interactive and non-interactive modes

**MUST NOT DO:**
- Print logs/diagnostics to stdout when output will be piped (use stderr)
- Break existing command signatures — treat renames as breaking changes
- Require interactive input in CI/CD without non-interactive flag fallbacks
- Hardcode platform-specific paths (use `os.homedir()` / `Path.home()`)
- Ship without shell completions

