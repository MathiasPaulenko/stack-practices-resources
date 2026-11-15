# LLM Guardrails Pattern — Companion Code

Runnable implementations for the [LLM Guardrails Pattern](https://stackpractices.com/patterns/llm-guardrails-pattern/) resource on StackPractices.

## Files

| File | What it shows |
| --- | --- |
| `llm_guardrails.py` | Self-contained demo: ordered input/output guardrail pipeline with fail-fast, prompt-injection / prohibited-content / input-PII checks, output toxicity and secret checks, and a full `GuardrailResult` audit trail. Runs with plain Python 3 — no API keys needed. |
| `llm-guardrails.js` | Same pipeline in Node.js. |
| `LLMGuardrailPipeline.java` | Same pipeline in Java 17+ (`javac` + `java`, no dependencies). |

## Quick start

```bash
python llm_guardrails.py
node llm-guardrails.js
javac LLMGuardrailPipeline.java && java LLMGuardrailPipeline
```

Expected output: one clean pass, three input-side blocks (injection, SSN,
prohibited word) and one output-side block — the model "leaks" an API key
and the output guardrail catches it. All calls are mocked, so results are
deterministic.

## What to adapt for production

- Replace the word lists and regex with your real layers: moderation API,
  a purpose-built injection classifier, your PII taxonomy. The pipeline
  shape stays — the checks are the part that evolves.
- Keep the cheap → expensive ordering: a 200ms classifier should only see
  traffic that survived free regex and length checks.
- Decide block vs. sanitize per category: the demo blocks everything for
  clarity; a production output guardrail would mask low-severity PII
  instead of throwing the whole response away.
- Send every `GuardrailResult` to your logs — category counts over time
  are how you tune rules and spot probing campaigns.
