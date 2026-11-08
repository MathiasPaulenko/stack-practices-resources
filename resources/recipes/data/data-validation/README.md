# Data Validation — Companion Examples

Runnable user-input validators referenced by the recipe
[Validate and Sanitize User Input Data](https://stackpractices.com/recipes/data-validation/).

## Files

| File | Stack | Run |
|------|-------|-----|
| `user_schema.ts` | Zod 4 (TypeScript) | `npx tsx user_schema.ts` |
| `user_model.py` | Pydantic v2 (Python) | `pip install "pydantic[email]" && python user_model.py` |
| `user_schema.js` | Joi 17 (Node.js) | `npm install joi && node user_schema.js` |

All three implement the same `User` schema — email, age range, role enum,
tag list — so you can compare syntax and error output side by side.
