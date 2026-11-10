# Environment Setup Guide Template — Companion Resources

Fillable guide for documenting reproducible environment setup: prerequisites, quick start, environment variables, verification, and troubleshooting.

## Files

- `environment-setup-guide-template.md` — blank guide template
- `Makefile` — one-command setup automation (`make setup`)
- `devcontainer.json` — VS Code devcontainer configuration
- `.env.example` — environment variable template with dummy values
- `example-filled.md` — the guide filled in for a fictional project

## Usage

Copy the template into your repository, run your own setup on a clean machine, and transcribe every command. Update the guide in the same PR as any change that affects setup steps. Never commit real secrets — use `.env.example` with dummy values.

Source: https://stackpractices.com/docs/environment-setup-guide-template/
