# Data Classification Template

Companion files for the [Data Classification Template](https://stackpractices.com/docs/data-classification-template/) on StackPractices.

## Files

| File | Purpose |
|------|---------|
| `data-classification-template.md` | Fillable template: four levels, dataset inventory, handling rules, exception log |
| `data-classification-example.md` | Completed example for a small B2B SaaS, with the non-obvious decisions documented |

## Usage

1. Copy `data-classification-template.md` into your wiki or security handbook.
2. Replace `<placeholders>` and fill the dataset inventory — export your datastore list first (RDS, S3, warehouses, SaaS tools) so nothing is missed.
3. Use `data-classification-example.md` as a reference for the level of reasoning each row deserves.
4. Wire the levels into enforcement: DLP rules, bucket policies, CI schema checks.
5. Review quarterly (Restricted), biannually (Confidential), annually (Internal/Public).

The four levels map to decisions engineers actually make: can I put this in a public ticket? Can I email it? Does it need an approval workflow?
