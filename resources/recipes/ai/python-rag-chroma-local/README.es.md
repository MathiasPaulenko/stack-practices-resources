# Pipeline RAG local con ChromaDB y Sentence Transformers

Codigo ejecutable que acompaña a la receta de StackPractices:
https://stackpractices.com/es/recipes/python-rag-chroma-local/

## Que contiene

- `rag_pipeline.py` — pipeline completo: chunking con overlap, store
  persistente con ChromaDB, generacion con OpenAI u Ollama y un reranker
  cross-encoder opcional.
- `requirements.txt` — dependencias fijadas.

## Instalacion

```bash
pip install -r requirements.txt
```

## Uso

Con OpenAI (necesita `OPENAI_API_KEY`):

```bash
export OPENAI_API_KEY=sk-...
python rag_pipeline.py
```

Totalmente local con Ollama (necesita `ollama serve` corriendo con `llama3` descargado):

```bash
python rag_pipeline.py --ollama
```

El script ingiere dos documentos de demo y responde una pregunta sobre Redis,
imprimiendo la respuesta generada y las fuentes usadas.

## Como adaptarlo

- Cambia `DEMO_DOCUMENTS` por tus propios dicts `{"title", "source", "text"}`.
- Cambia `persist_dir` para guardar el vector store fuera del directorio de trabajo.
- Usa `RerankedRAG` en lugar de `RAGPipeline` para activar el reranking con cross-encoder.
- Usa `query_with_filter()` para acotar la recuperacion por metadatos de `source`.
