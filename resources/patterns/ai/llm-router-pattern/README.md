# LLM Router Pattern — Companion Code

Runnable implementations for the [LLM Router Pattern](https://stackpractices.com/patterns/llm-router-pattern/) resource on StackPractices.

## Files

| File | What it shows |
| --- | --- |
| `llm_router.py` | Self-contained demo: rules-based complexity classifier with confidence, one-shot tier routing, and a `CascadeRouter` that starts one tier lower on low confidence and escalates through a quality gate. Tracks routed cost against an always-large baseline. Runs with plain Python 3 — no API keys needed. |
| `llm-router.js` | Same router + cascade in Node.js. |
| `LLMRouterCascade.java` | Same router + cascade in Java 17+ (`javac` + `java`, no dependencies). |

## Quick start

```bash
python llm_router.py
node llm-router.js
javac LLMRouterCascade.java && java LLMRouterCascade
```

Expected output: the one-shot router sends low queries to `gpt-4o-mini`
and medium ones to `gpt-4o` (~81% cheaper than always-large). The cascade
variant starts borderline queries one tier lower, catches the thin
responses, and escalates — same quality, three extra calls, ~83% saved.
All calls are mocked, so results are deterministic.

## What to adapt for production

- Replace `mockGenerate` / `mock_generate` with real provider calls; the
  routing contract (level + confidence → tier) doesn't change.
- The rules classifier is a floor, not a ceiling — climb to embedding or
  LLM classification only when the savings justify the added latency.
- Bias thresholds toward the bigger model: under-routing ships a wrong
  answer quietly; over-routing just costs more. When unsure, route up or
  use the cascade.
- Keep the baseline tracker — "cost vs. always-large" is the number that
  justifies the router internally, and you can't tune thresholds you
  can't see.
