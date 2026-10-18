# Database Schema Documentation Template

A copy-paste-ready Markdown template for documenting database schemas: entity definitions, relationships, index rationale, enum references, migration history, and deprecated columns.

Source article: https://stackpractices.com/docs/database-schema-documentation-template/

## Files

| File | Description |
|------|-------------|
| `template.md` | The schema documentation template, pre-filled with a realistic e-commerce example (users, orders, order_items, user_preferences). Replace the example with your own tables. |
| `example-schema.dbml` | The same example schema in DBML. Paste it into [dbdiagram.io](https://dbdiagram.io/d) to render the ER diagram. |

## Usage

1. Copy `template.md` into your repo (e.g., `docs/schema.md`).
2. Replace the `[Database Name]` placeholder and the overview fields.
3. Document each table: purpose, columns, constraints, indexes, business rules.
4. Fill in the relationships section and the enum reference.
5. Keep the migration history table updated with every schema change.
6. Optionally, keep `example-schema.dbml` alongside and update it in the same PR.

To generate docs automatically from a live database, use this template as the narrative layer on top of [tbls](https://github.com/k1LoW/tbls) or [dbdocs](https://dbdocs.io) output.
