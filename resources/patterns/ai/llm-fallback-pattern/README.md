# LLM Fallback Pattern — Companion Code

Runnable implementations for the [LLM Fallback Pattern](https://stackpractices.com/patterns/llm-fallback-pattern/) resource on StackPractices.

## Files

| File | What it shows |
| --- | --- |
| `llm_fallback.py` | Self-contained demo: provider chain with per-provider retry budgets, retryable/non-retryable error taxonomy, `CircuitBreaker` + `BreakerChain` integration, and a static last-resort response. Runs with plain Python 3 — no API keys needed. |
| `llm-fallback.js` | Same chain in Node.js (async/await version). |
| `LLMFallbackChain.java` | Same chain in Java 17+ (`javac` + `java`, no dependencies). |

## Quick start

```bash
python llm_fallback.py
node llm-fallback.js
javac LLMFallbackChain.java && java LLMFallbackChain
```

Expected output: a clean call on `openai`, a rate-limit storm that retries
twice and falls back to `anthropic`, and the remaining prompts served by the
primary. All provider calls are mocked, so failures are deterministic.

## What to adapt for production

- Replace `mock_provider_call` with one adapter per real provider that maps
  its SDK errors into the shared `ErrorType` taxonomy — that mapping is the
  load-bearing part of the pattern.
- Add a chain-wide deadline so the worst case isn't the sum of every
  provider's worst case.
- Emit a metric on every fallthrough; a fallback rate alert catches provider
  outages before the invoice does.
