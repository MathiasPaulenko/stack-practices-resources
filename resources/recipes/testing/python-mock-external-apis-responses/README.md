# Mock External APIs with responses — Runnable Examples

Companion code for the StackPractices recipe
[Mock External APIs with responses Library](https://stackpractices.com/recipes/python-mock-external-apis-responses/).

## Files

| File | What it shows |
|------|---------------|
| `test_external_api.py` | 10 runnable tests: basic mock, `matchers` (query params), error/timeout simulation, ordered retry sequence, dynamic `add_callback`, request-body assertion, regex URL matching, streaming generator, shared fixture |
| `conftest.py` | `mock_api` fixture wrapping `responses.RequestsMock()` for reuse across tests |
| `requirements.txt` | `pytest`, `requests`, `responses>=0.25` |

## Run

```bash
pip install -r requirements.txt
pytest -v
```

## Key detail

`match_querystring` was deprecated in responses 0.17.0 — use
`matchers.query_param_matcher` in the `match` list instead. Registered
responses for the same URL are consumed in order, which is how the retry
sequence test returns 503 then 200.
