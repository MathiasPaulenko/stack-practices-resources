"""Pinecone vector store: index, upsert, query, filter, namespaces, hybrid search.

Runnable single-file version of the StackPractices recipe
"Store and Query Embeddings in Pinecone Vector Database".

Requires PINECONE_API_KEY and OPENAI_API_KEY environment variables.
"""

import os
import time
import uuid

from openai import OpenAI
from pinecone import Pinecone, ServerSpec, SparseValues

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
INDEX_NAME = "knowledge-base"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536

pc = Pinecone(api_key=PINECONE_API_KEY)
openai_client = OpenAI()


def get_or_create_index(index_name: str = INDEX_NAME):
    """Create the serverless index if missing and return a handle to it."""
    if index_name not in [idx.name for idx in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerSpec(cloud="aws", region="us-east-1"),
        )
    return pc.Index(index_name)


index = get_or_create_index()


def generate_embedding(text: str) -> list[float]:
    """Generate embedding using OpenAI."""
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


def upsert_documents(documents: list[dict]) -> dict:
    """Upsert documents with embeddings and metadata.

    Args:
        documents: List of {text, metadata} dicts.

    Returns:
        Upsert response from Pinecone.
    """
    vectors = []
    for doc in documents:
        embedding = generate_embedding(doc["text"])
        vectors.append(
            {
                "id": doc.get("id", str(uuid.uuid4())),
                "values": embedding,
                "metadata": {
                    **doc.get("metadata", {}),
                    "text": doc["text"][:500],
                },
            }
        )
    return index.upsert(vectors=vectors)


def search_similar(
    query: str,
    top_k: int = 5,
    metadata_filter: dict | None = None,
) -> list[dict]:
    """Search for similar documents.

    Args:
        query: Query text.
        top_k: Number of results to return.
        metadata_filter: Metadata filter dict.

    Returns:
        List of {id, score, metadata} dicts.
    """
    query_embedding = generate_embedding(query)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=metadata_filter,
    )
    return [
        {
            "id": match["id"],
            "score": match["score"],
            "metadata": match["metadata"],
        }
        for match in results["matches"]
    ]


def upsert_to_namespace(documents: list[dict], namespace: str) -> dict:
    """Upsert documents to a specific namespace."""
    vectors = []
    for doc in documents:
        embedding = generate_embedding(doc["text"])
        vectors.append(
            {
                "id": doc["id"],
                "values": embedding,
                "metadata": doc.get("metadata", {}),
            }
        )
    return index.upsert(vectors=vectors, namespace=namespace)


def search_namespace(query: str, namespace: str, top_k: int = 5) -> list[dict]:
    """Search within a specific namespace."""
    query_embedding = generate_embedding(query)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace,
    )
    return results["matches"]


def batch_upsert(documents: list[dict], batch_size: int = 100) -> int:
    """Upsert documents in batches to avoid rate limits.

    Args:
        documents: List of documents to upsert.
        batch_size: Number of vectors per batch.

    Returns:
        Total number of vectors upserted.
    """
    total = 0
    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        texts = [doc["text"] for doc in batch]
        response = openai_client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts,
        )
        embeddings = [item.embedding for item in response.data]
        vectors = [
            {
                "id": doc.get("id", str(uuid.uuid4())),
                "values": emb,
                "metadata": doc.get("metadata", {}),
            }
            for doc, emb in zip(batch, embeddings)
        ]
        index.upsert(vectors=vectors)
        total += len(vectors)
        print(f"Upserted batch {i // batch_size + 1}: {total} total")
    return total


def upsert_with_retry(vectors: list[dict], attempts: int = 3) -> dict:
    """Upsert with exponential backoff on transient failures."""
    for attempt in range(1, attempts + 1):
        try:
            return index.upsert(vectors=vectors)
        except Exception as exc:
            if attempt == attempts:
                raise
            wait = 2**attempt
            print(f"Upsert failed ({exc}), retrying in {wait}s")
            time.sleep(wait)


def delete_by_filter(metadata_filter: dict) -> dict:
    """Delete all vectors matching a metadata filter."""
    return index.delete(filter=metadata_filter)


def fetch_vectors(ids: list[str]) -> dict:
    """Fetch vectors by their IDs."""
    return index.fetch(ids=ids)


def upsert_hybrid(
    doc_id: str,
    text: str,
    dense_values: list[float],
    sparse_values: dict,
) -> dict:
    """Upsert one document with dense and sparse vectors."""
    return index.upsert(
        vectors=[
            {
                "id": doc_id,
                "values": dense_values,
                "sparse_values": SparseValues(
                    indices=sparse_values["indices"],
                    values=sparse_values["values"],
                ),
                "metadata": {"text": text},
            }
        ]
    )


def main() -> None:
    """Minimal end-to-end demo: upsert, wait, query, check stats."""
    upsert_documents(
        [
            {
                "id": "doc1",
                "text": "Redis is an in-memory data structure store used as a cache and database.",
                "metadata": {"category": "database", "source": "docs"},
            },
            {
                "id": "doc2",
                "text": "PostgreSQL is a capable open-source relational database system.",
                "metadata": {"category": "database", "source": "docs"},
            },
            {
                "id": "doc3",
                "text": "Docker containers package applications with their dependencies.",
                "metadata": {"category": "devops", "source": "tutorial"},
            },
        ]
    )

    # Fresh writes take a few seconds to become queryable
    time.sleep(5)
    stats = index.describe_index_stats()
    print(f"Total vectors: {stats['total_vector_count']}")

    results = search_similar("in-memory cache for fast lookups", top_k=3)
    for r in results:
        print(f"Score: {r['score']:.3f} | {r['metadata']['text'][:80]}")

    filtered = search_similar(
        "database for web applications",
        top_k=5,
        metadata_filter={"category": {"$eq": "database"}},
    )
    print(f"Filtered hits: {len(filtered)}")


if __name__ == "__main__":
    main()
