# Input Validation — Companion Resources

Runnable examples for the [input validation recipe](https://stackpractices.com/recipes/input-validation/) on StackPractices.

Schema-first validation: declare the shape once, let the library reject malformed input at the boundary, and return field-level errors the client can render next to each input.

## Files

| File | What it shows |
|------|---------------|
| `validate_user.py` | Pydantic v2 model with `Field` constraints, `field_validator`, `EmailStr`, and a `format_errors()` helper that turns `ValidationError` into a 400-ready payload |
| `test_validate_user.py` | pytest suite: valid path, blank-name rejection, email/age bounds, error aggregation |
| `validate_user.js` | Zod schema with `safeParse` and a `validateUser()` wrapper that returns `{ data }` or `{ errors }` |
| `validate_user.test.js` | `node:test` suite mirroring the Python tests |

## Run it

```bash
# Python (requires pydantic[email] + pytest)
pip install -r requirements.txt
python validate_user.py
python -m pytest test_validate_user.py -v

# JavaScript (Node 18+)
npm install
node validate_user.js
node --test validate_user.test.js
```

## Key takeaways

- Validate at the boundary; the service layer should receive typed objects, not raw strings.
- `safeParse` / `ValidationError` aggregate *all* violations — users fix three fields in one round trip.
- Coercion is explicit: `"36"` becomes `36` only where the schema allows it.
- Validation isn't sanitization — escape output per context and parameterize queries separately.

CI: `.github/workflows/test.yml` runs both suites on every change to this folder.
