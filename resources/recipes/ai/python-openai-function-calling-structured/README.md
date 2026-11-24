# Structured JSON Output from OpenAI Function Calling

Runnable companion code for the StackPractices recipe
[Structured JSON Output from OpenAI Function Calling](https://stackpractices.com/recipes/python-openai-function-calling-structured/).

## Contents

- `structured_extract.py` — Pydantic schemas (`ProductReview`, `SearchQuery`,
  `CalculationRequest`), function-calling extraction, `response_format` with
  `json_schema` + `strict`, retry with exponential backoff on
  `RateLimitError`, refusal handling, and batch extraction.
- `main.py` — demo that extracts a typed `ProductReview` from free-text input.
- `requirements.txt` — pinned dependencies (`openai`, `pydantic`).

## Usage

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python main.py
```

Requires an OpenAI API key. See the recipe for the full explanation of
strict mode, refusals, and retry semantics.
