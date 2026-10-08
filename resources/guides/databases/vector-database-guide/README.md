# Vector Database — pgvector RAG Pipeline

Runnable pgvector RAG pipeline: a Postgres + pgvector container, schema with a tuned HNSW index, chunked ingestion with OpenAI embeddings, and a query script that answers with source citations.

Companion code for the StackPractices guide:
[Vector Databases in Practice: Embeddings & Similarity Search](https://stackpractices.com/guides/vector-database-guide/)

## Setup

```bash
docker compose up -d          # Postgres 16 + pgvector, schema auto-applied
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

## Usage

```bash
mkdir docs && cp /path/to/*.md docs/   # add your documents
python ingest.py docs/                 # chunk, embed, store
python query.py "How do vector indexes work?"
```

## Files

| File | Contents |
|---|---|
| `docker-compose.yml` | pgvector/pgvector:pg16 container |
| `schema.sql` | `doc_chunks` table + HNSW index (m=16, ef_construction=64) |
| `ingest.py` | Chunking (~500 tokens, 10% overlap) + embedding + insert |
| `query.py` | `rag_query`: similarity search + GPT-4o answer with citations |
| `requirements.txt` | openai, psycopg2-binary, pgvector |

## Notes

- `register_vector(conn)` from the `pgvector` package is required for psycopg2 to serialize `list[float]` into the vector type.
- Embeddings are model-specific: if you change `text-embedding-3-small` for another model, re-embed everything — vectors are not comparable across models.
- Tune `ef_search` at query time (`SET hnsw.ef_search = 40`) to trade recall for latency.
