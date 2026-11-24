# Local RAG Pipeline with ChromaDB and Sentence Transformers

Runnable companion code for the StackPractices recipe:
https://stackpractices.com/recipes/python-rag-chroma-local/

## What it contains

- `rag_pipeline.py` — complete pipeline: chunking with overlap, ChromaDB
  persistent store, OpenAI and Ollama generation backends, and an optional
  cross-encoder reranker.
- `requirements.txt` — pinned dependencies.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

With OpenAI (needs `OPENAI_API_KEY`):

```bash
export OPENAI_API_KEY=sk-...
python rag_pipeline.py
```

Fully local with Ollama (needs `ollama serve` running with `llama3` pulled):

```bash
python rag_pipeline.py --ollama
```

The script ingests two demo documents and answers a question about Redis,
printing the generated answer and the sources used.

## Adapting it

- Swap `DEMO_DOCUMENTS` for your own `{"title", "source", "text"}` dicts.
- Change `persist_dir` to keep the vector store out of your working tree.
- Use `RerankedRAG` instead of `RAGPipeline` to enable cross-encoder reranking.
- Use `query_with_filter()` to scope retrieval by `source` metadata.
