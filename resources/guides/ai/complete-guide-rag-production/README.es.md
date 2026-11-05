# RAG en Producción — Companion

Código ejecutable de [Guía Completa de RAG en Producción](https://stackpractices.com/es/guides/complete-guide-rag-production/).

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `chunking.py` | Chunking de tamaño fijo, por oraciones, semántico y consciente de markdown |
| `embeddings.py` | Embeddings locales con sentence-transformers + batch de OpenAI (`asyncio.gather`) |
| `vector_stores.py` | Stores Chroma, Pinecone y pgvector tras una interfaz con formato Chroma |
| `hybrid_search.py` | Fusión ponderada `HybridSearch`, `SimpleKeywordIndex` y RRF |
| `rerankers.py` | Reranking con cross-encoder (self-hosted) y API hosted de Cohere |
| `context_assembly.py` | Ensamblado de contexto con presupuesto de tokens (tiktoken) + prompt |
| `rag_pipeline.py` | Pipeline completo embed → retrieve → rerank → generate (`asyncio.to_thread`) |
| `evaluation.py` | Runner de RAGAS — faithfulness, answer relevancy, context precision/recall |
| `test_rag.py` | Tests unitarios offline — sin API key ni descargas de modelos |
| `tests.json` | Dataset de evaluación RAGAS de ejemplo |
| `requirements.txt` | Dependencias fijadas |

## Inicio rápido

```bash
pip install -r requirements.txt
pytest test_rag.py -v        # corre completamente offline
python rag_pipeline.py       # demo offline con modelos stub
python chunking.py           # demo de chunking offline
export OPENAI_API_KEY=sk-... # necesario para embeddings/LLM reales
export COHERE_API_KEY=...    # solo para cohere_rerank
python evaluation.py         # necesita un LLM configurado para RAGAS
```

Notas:

- `vector_stores.py`: Chroma funciona localmente sin configuración; Pinecone necesita `PINECONE_API_KEY`, pgvector necesita un Postgres con la extensión `vector`.
- `embeddings.py`: `local_embed()` descarga el modelo en el primer uso; `batch_embed()` necesita `OPENAI_API_KEY`.
- `context_assembly.py` descarga el encoding de tiktoken en el primer uso real.
- Nunca cambies el modelo de embeddings sin re-embeber todo el corpus — los vectores de modelos distintos no son comparables.
