# Prompt Chaining Pattern — Companion Resources

Companion files for the [Prompt Chaining Pattern](https://stackpractices.com/patterns/prompt-chaining-pattern/) on StackPractices.com.

## What's included

| File | Language | Description |
|------|----------|-------------|
| `prompt_chain.py` | Python | `PromptChain` class with `ChainStep` dataclass, validators, retry logic |
| `prompt_chain.js` | JavaScript | `PromptChain` class with async `run()`, validators, retry logic |
| `PromptChaining.java` | Java | `PromptChaining` with `ChainStep`/`ChainResult` records, `Predicate` validators |

## Quick start

### Python

```bash
python prompt_chain.py
```

### JavaScript

```bash
node prompt_chain.js
```

### Java

```bash
javac PromptChaining.java && java PromptChaining
```

## How it works

1. Define chain steps with a name, prompt template, model, temperature, and optional validator
2. The chain runs steps sequentially: each step's output feeds the next step's input
3. If a step's validator fails, the step retries up to `max_retries` times
4. If all retries fail, the chain stops and returns partial results

## Replacing the mock

The `mock_llm_call` / `mockLlmCall` function simulates an LLM API call. Replace it with your actual client:

- **Python**: `openai.chat.completions.create()` or `anthropic.messages.create()`
- **JavaScript**: `openai.chat.completions.create()` or `@anthropic-ai/sdk`
- **Java**: OpenAI Java SDK or Anthropic Java SDK

## References

- [OpenAI prompt engineering guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [LangChain chains documentation](https://python.langchain.com/docs/modules/chains/)
- [Anthropic chain prompts guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)
