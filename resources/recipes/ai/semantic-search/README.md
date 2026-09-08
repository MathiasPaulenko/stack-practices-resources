# Semantic Search — Companion Examples

Companion code for the [Semantic Search recipe](https://stackpractices.com/recipes/semantic-search/).

## Files

| File | Description |
|------|-------------|
| `semantic_search_faiss.py` | Local semantic search with sentence-transformers + FAISS (free, no API key) |
| `semantic_search_openai.py` | Semantic search with OpenAI embeddings + FAISS (requires `OPENAI_API_KEY`) |
| `semantic_search_js.js` | JavaScript semantic search with OpenAI + cosine similarity |
| `SemanticSearchService.java` | Java Spring AI + pgvector production service |
| `test_semantic_search.py` | Unit tests (run without external dependencies) |

## Quick start (local FAISS)

```bash
pip install sentence-transformers faiss-cpu numpy
python semantic_search_faiss.py
```

## Quick start (OpenAI)

```bash
pip install openai faiss-cpu numpy
export OPENAI_API_KEY="your-key"
python semantic_search_openai.py
```

## Run tests

```bash
pip install pytest numpy
pytest test_semantic_search.py -v
```

## Author

Mathias Paulenko — [StackPractices.com](https://stackpractices.com)
