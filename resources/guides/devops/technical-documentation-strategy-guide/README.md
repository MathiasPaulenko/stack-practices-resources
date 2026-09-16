# Technical Documentation Strategy: Docs as Code — Templates

Companion resources for the guide
[Technical Documentation Strategy: Docs as Code](https://stackpractices.com/guides/technical-documentation-strategy-guide/).

## Contents

| File | Purpose |
|------|---------|
| `readme-template.md` | Service README skeleton answering the questions a newcomer asks, in order. |
| `adr-template.md` | Architecture Decision Record template: Status, Context, Decision, Consequences. |
| `runbook-template.md` | Symptom-keyed runbook template: Symptoms → Diagnosis → Resolution → Escalation. |
| `codeowners-example` | `CODEOWNERS` example that assigns doc ownership per path. |
| `stale-docs-check.sh` | Bash script that lists Markdown files not modified in N days (default 365). |

## Usage

Copy the templates into your service repos and adapt them:

```bash
cp readme-template.md /path/to/service/README.md
cp adr-template.md /path/to/service/adr/001-my-decision.md
cp runbook-template.md /path/to/service/runbook.md
cp codeowners-example /path/to/service/.github/CODEOWNERS
```

Run the stale-docs check quarterly and assign the output to owners:

```bash
./stale-docs-check.sh 365 ./services
```

## License

See the repository root `LICENSE`.
