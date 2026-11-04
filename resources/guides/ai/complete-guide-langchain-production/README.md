# LangChain in Production — Companion

Runnable Python project from the StackPractices guide
[Complete Guide to LangChain in Production](https://stackpractices.com/guides/complete-guide-langchain-production/).

## Files

| File | Description |
|------|-------------|
| `chain.py` | Basic LCEL chain: prompt → model → parser |
| `parallel_chain.py` | `RunnableParallel` fan-out (summary + keywords + sentiment) |
| `rag.py` | Full RAG pipeline: load → split → Chroma → retrieve → cited answer |
| `agent.py` | Tool-calling agent with `max_iterations`/`max_execution_time` and safe `asteval` math |
| `app.py` | FastAPI endpoint streaming the chain over SSE |
| `test_chain.py` | Unit tests with `FakeListChatModel` — zero API calls |
| `requirements.txt` | Pinned dependencies including partner packages |

## Quick start

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...

# Run the pieces
python chain.py
python parallel_chain.py
python agent.py

# RAG needs a doc to index
mkdir -p docs && echo "Vacation policy: 20 days per year." > docs/handbook.txt
python rag.py

# Serve the API
uvicorn app:app --reload

# Tests run without an API key
pytest test_chain.py -v
```

`test_chain.py` and its fallback test run fully offline. Everything else
requires `OPENAI_API_KEY`.
