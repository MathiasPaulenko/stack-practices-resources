# API Security Review Template — Companion Resources

Fillable API security review checklist mapped to the OWASP API Security Top 10 (2023), plus a complete worked example.

## Files

- `api-security-review-template.md` — the blank checklist: metadata, authentication, authorization, input validation, rate limiting tiers, secrets management, data protection, error handling and logging, OWASP API Top 10 coverage table, and a findings/sign-off section.
- `example-filled.md` — the same template completed for a fictional public REST API (`payments-api`), showing how unchecked boxes turn into a findings table with severity, owner, and due date.

## How to use

1. Copy `api-security-review-template.md` into your repo, wiki, or a ticket.
2. Fill the metadata and work through each section for one API (or one endpoint group).
3. Move every unchecked box into the findings table with a severity, owner, and due date.
4. Archive the completed review — auditors ask for evidence, not intentions.

Source: [API Security Review Template](https://stackpractices.com/docs/api-security-review-template/)
