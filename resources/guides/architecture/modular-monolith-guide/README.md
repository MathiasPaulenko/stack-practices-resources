# Modular Monolith Guide — Companion Code

A runnable, dependency-free implementation of the boundary enforcement described in the [Modular Monolith guide](https://stackpractices.com/guides/modular-monolith-guide/): a linter that walks a `modules/` tree, resolves every import, and reports any module that reaches into another module's internals instead of its public `api`.

## Files

| File | Stack | Tests |
|------|-------|-------|
| `boundary_check.py` | Python stdlib (`re`, `pathlib`, `unittest`) | 4 unittest cases |
| `boundary_check.mjs` | Node.js (`node:test`, `node:assert`, `node:fs`) | 4 cases under `node --test` |

## Run

```bash
# Test suites
python -m unittest boundary_check -v
node --test boundary_check.mjs

# Lint a real codebase (Python version also works as a CLI)
python boundary_check.py /path/to/your-project
```

## The rule it enforces

- `modules/<name>/api/` is the only public surface — other modules may import it.
- `shared/kernel/` is shared by everyone, both directions.
- Any import that crosses a module line into `domain/`, `application/`, or `infrastructure/` is a violation: the file, line, and offending import get reported.

## Why a test and not a convention

A boundary that only lives in a style guide erodes within months — someone on a deadline imports another module's repository "just this once". A failing CI check turns "please don't" into "can't merge", which is the actual point of the pattern.
