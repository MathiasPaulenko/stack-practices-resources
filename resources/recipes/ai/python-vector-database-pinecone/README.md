# Pinecone Vector Store with OpenAI Embeddings

Runnable companion for the StackPractices recipe
[Store and Query Embeddings in Pinecone Vector Database](https://stackpractices.com/recipes/python-vector-database-pinecone/).

Single-file implementation covering:

- Serverless index creation (1536 dims, cosine metric)
- OpenAI `text-embedding-3-small` embeddings + upsert with metadata
- Similarity search with metadata filtering (`$eq`, `$gte`, `$in`…)
- Namespaces for multi-tenant isolation
- Batch upserts with exponential-backoff retries
- Hybrid dense + sparse search (`SparseValues`)
- Delete by filter, fetch by ID, `describe_index_stats()`

## Setup

```bash
pip install -r requirements.txt
export PINECONE_API_KEY="your-pinecone-api-key"
export OPENAI_API_KEY="your-openai-api-key"
python pinecone_vector_store.py
```

`main()` runs a minimal demo: it upserts three sample documents, waits for
propagation, prints index stats, and runs an unfiltered and a filtered query.

## Notes

- Free tier covers one serverless index with 100K vectors.
- Freshly upserted vectors take a few seconds to become queryable — poll
  `describe_index_stats()` instead of asserting on query results.
- Switching to `text-embedding-3-large` requires a new index at 3072 dimensions.
