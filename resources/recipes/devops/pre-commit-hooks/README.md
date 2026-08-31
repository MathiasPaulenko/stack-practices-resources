# Pre-Commit Hooks — Runnable Examples

Companion code for the StackPractices recipe:  
https://stackpractices.com/recipes/pre-commit-hooks/

## What's inside

| File | Purpose |
|---|---|
| `.pre-commit-config.yaml` | Python `pre-commit` framework with black, flake8, mypy and gitleaks |
| `package.json` | Node setup for husky, lint-staged, simple-git-hooks and commitlint |
| `.husky/pre-commit` | Husky v9 pre-commit hook |
| `.lintstagedrc.js` | lint-staged config for JS/TS and JSON/Markdown/YAML |
| `commitlint.config.js` | Conventional commit lint rules |
| `build.gradle` | Java/Gradle Spotless formatting check |
| `lefthook.yml` | Cross-language hook manager config |
| `.gitattributes` | LF line endings for shell scripts |

## How to use

### Python

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### Node with husky

```bash
npm install
npx husky init
```

Replace `.husky/pre-commit` with the sample in this repo.

### Node with simple-git-hooks

```bash
npm install
npx simple-git-hooks
```

### Java with Gradle

```bash
./gradlew spotlessCheck
# To fix formatting:
# ./gradlew spotlessApply
```

### Cross-language with lefthook

```bash
lefthook install
lefthook run pre-commit
```

## Do not commit directly to `.git/hooks`

The hook scripts themselves live in `.git/hooks/` and are not tracked. The configuration files in this repo are tracked and used by the tools above to install the hooks automatically.

## License

MIT — use at your own risk in your own projects.
