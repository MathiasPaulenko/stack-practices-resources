# RAG in Production — Companion

Runnable code from [Complete Guide to RAG in Production](https://stackpractices.com/guides/complete-guide-rag-production/).

## Files

| File | Description |
|------|-------------|
| `chunking.py` | Fixed-size, sentence, semantic, and markdown-aware chunking |
| `embeddings.py` | Local sentence-transformers + OpenAI batch embedding (`asyncio.gather`) |
| `vector_stores.py` | Chroma, Pinecone, and pgvector stores behind one Chroma-shaped interface |
| `hybrid_search.py` | `HybridSearch` weighted fusion, `SimpleKeywordIndex`, and RRF |
| `rerankers.py` | Cross-encoder (self-hosted) and Cohere hosted reranking |
| `context_assembly.py` | Token-budgeted context assembly with tiktoken + prompt builder |
| `rag_pipeline.py` | Full embed → retrieve → rerank → generate pipeline (`asyncio.to_thread`) |
| `evaluation.py` | RAGAS runner — faithfulness, answer relevancy, context precision/recall |
| `test_rag.py` | Offline unit tests — no API key or model downloads |
| `tests.json` | Sample RAGAS eval dataset |
| `requirements.txt` | Pinned dependencies |

## Quick start

```bash
pip install -r requirements.txt
pytest test_rag.py -v        # runs fully offline
python rag_pipeline.py       # offline demo with stub models
python chunking.py           # offline chunking demo
export OPENAI_API_KEY=sk-... # needed for real embeddings/LLM calls
export COHERE_API_KEY=...    # only for cohere_rerank
python evaluation.py         # needs an LLM configured for RAGAS
```

Notes:

- `vector_stores.py`: Chroma works locally out of the box; Pinecone needs `PINECONE_API_KEY`, pgvector needs a Postgres with the `vector` extension.
- `embeddings.py`: `local_embed()` downloads the model on first use; `batch_embed()` needs `OPENAI_API_KEY`.
- `context_assembly.py` downloads the tiktoken encoding on first real use.
- Never swap embedding models without re-embedding the whole corpus — vectors from different models aren't comparable.
