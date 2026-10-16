# Compose LCEL Chains in LangChain — Companion Project

Runnable companion for the [LCEL chains recipe](https://stackpractices.com/recipes/python-langchain-chains-composition/) on StackPractices. It shows how to organize chains across files, which the recipe FAQ mentions without a full project layout.

## Contents

| File | What it is |
|------|------------|
| `chains.py` | Chain factories: `basic_chain`, `summarize_then_translate_chain`, `parallel_analysis_chain`, `custom_components_chain`, `resilient_chain` (retry + fallback), `routing_chain`. Each returns a `Runnable` you can pipe or import elsewhere. |
| `main.py` | Entry point that invokes every chain variant, including a `batch` example. |
| `requirements.txt` | `langchain`, `langchain-openai`, `langchain-core`, `pydantic`. |

## Run it

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python main.py
```

Adapt the model names and prompts to your provider. Any `BaseChatModel` works — Anthropic, Google, or local models via `langchain-ollama`.

Source recipe: https://stackpractices.com/recipes/python-langchain-chains-composition/
