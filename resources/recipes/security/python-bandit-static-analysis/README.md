# Bandit static analysis — companion files

Files referenced by the recipe
[Find Security Issues in Python Code with Bandit](https://stackpractices.com/recipes/python-bandit-static-analysis/).

| File | Purpose |
| --- | --- |
| `bandit.ini` | Project-root `.bandit` config: path exclusions only, all checks enabled. |
| `pyproject.toml` | TOML alternative (`[tool.bandit]`); load with `bandit -c pyproject.toml -r src/`. |
| `pre-commit-config.yaml` | pre-commit hook pinned to a released Bandit version. |
| `bandit-workflow.yml` | GitHub Actions job that fails on findings at the chosen severity and uploads the JSON report. |
| `bandit_plugins/no_print_statements.py` | Custom check registered via the `bandit.plugins` entry-point group. |

## Notes

- The baseline file is generated in your own repo: `bandit -r src/ -f json -o .bandit-baseline.json --exit-zero`, then `bandit -r src/ -b .bandit-baseline.json`.
- Custom plugins must be importable in the environment running Bandit; package and install them, do not pass file paths to the CLI.
