# Kafka Topic Naming Convention — Companion Files

Files accompanying the StackPractices template: a lint script that validates topic names against `<env>.<domain>.<entity>.<type>[.<version>]`, a ready-to-fill topic request ticket, and Terraform `kafka_topic` examples.

Companion to: https://stackpractices.com/docs/kafka-topic-naming-convention-template/

## Files

- `naming-lint.sh` — validates topic names from stdin, exits non-zero on violations
- `topics.txt` — sample topic list (mix of valid and invalid names)
- `kafka-topics.tf` — Terraform examples for event, snapshot (compacted), and DLQ topics
- `topic-request-template.md` — ticket template for the creation workflow

## Run the linter

```bash
./naming-lint.sh < topics.txt
```

Expected output: the first six names pass, the last five fail with the reason.
