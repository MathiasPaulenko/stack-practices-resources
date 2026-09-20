# RAG Pipeline with LangChain and Vector Databases

Runnable companion for [Build a RAG Pipeline with LangChain and Vector Databases](https://stackpractices.com/recipes/rag-pipeline/).

## What's included

- `rag_pipeline.py` — full pipeline: load → chunk → embed → store in Chroma → retrieve → generate, with a fallback prompt that answers "I don't know" when context is missing.
- `evaluate.py` — minimal retrieval evaluation: runs a small question set against the persisted store and reports hit rate.
- `knowledge_base.txt` — sample corpus (refunds, warranty, shipping, support, accounts).
- `requirements.txt` — pinned LangChain/Chroma dependencies.

## Requirements

- Python 3.10+
- An OpenAI API key (`OPENAI_API_KEY`) — used for embeddings and `gpt-4o-mini` generation.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python rag_pipeline.py   # ingest + two answered questions + one fallback question
python evaluate.py       # retrieval hit-rate check
```

## Notes

- Uses current LangChain packages (`langchain-openai`, `langchain-chroma`, `langchain-community`). Legacy imports like `from langchain.embeddings import OpenAIEmbeddings` are removed in recent versions.
- To use a local embedding model instead of OpenAI, swap `OpenAIEmbeddings` for `HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")` from `langchain-huggingface` — no API key needed.
