"""Semantic similarity search with OpenAI embeddings and cosine similarity.

Provides embedding helpers (single, batch, retry-with-backoff), cosine
similarity functions (scalar and pairwise matrix), a minimal in-memory
similarity search index, and threshold-based deduplication.
"""

import time
from dataclasses import dataclass

import numpy as np
from openai import OpenAI, RateLimitError

client = OpenAI()

DEFAULT_MODEL = "text-embedding-3-small"


def get_embedding(text: str, model: str = DEFAULT_MODEL) -> list[float]:
    """Generate an embedding for a single text."""
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding


def get_embeddings_batch(
    texts: list[str], model: str = DEFAULT_MODEL
) -> list[list[float]]:
    """Generate embeddings for a batch of texts in one API call."""
    response = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in response.data]


def embed_with_retry(texts: list[str], retries: int = 3) -> list[list[float]]:
    """Embed texts, retrying on rate limits with exponential backoff."""
    for attempt in range(retries):
        try:
            return get_embeddings_batch(texts)
        except RateLimitError:
            if attempt == retries - 1:
                raise
            time.sleep(2**attempt)
    return []


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute cosine similarity between two vectors (-1 to 1)."""
    a = np.array(vec_a)
    b = np.array(vec_b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def cosine_similarity_matrix(vectors: list[list[float]]) -> np.ndarray:
    """Compute the pairwise NxN cosine similarity matrix."""
    matrix = np.array(vectors)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    normalized = np.divide(matrix, norms, out=np.zeros_like(matrix), where=norms > 0)
    return normalized @ normalized.T


def euclidean_distance(vec_a: list[float], vec_b: list[float]) -> float:
    """Compute Euclidean distance between two vectors."""
    return float(np.linalg.norm(np.array(vec_a) - np.array(vec_b)))


@dataclass
class Document:
    id: str
    text: str
    embedding: list[float]


class SimilaritySearchIndex:
    """In-memory similarity search over embedded documents."""

    def __init__(self):
        self.documents: list[Document] = []

    def add(self, doc_id: str, text: str) -> None:
        """Embed one document and add it to the index."""
        embedding = get_embedding(text)
        self.documents.append(Document(id=doc_id, text=text, embedding=embedding))

    def add_batch(self, items: list[tuple[str, str]]) -> None:
        """Embed and add several documents with a single batched call."""
        texts = [text for _, text in items]
        embeddings = get_embeddings_batch(texts)
        for (doc_id, text), emb in zip(items, embeddings):
            self.documents.append(Document(id=doc_id, text=text, embedding=emb))

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Return the top_k most similar documents for a query."""
        query_emb = get_embedding(query)
        scores = [
            (doc.id, doc.text, cosine_similarity(query_emb, doc.embedding))
            for doc in self.documents
        ]
        scores.sort(key=lambda x: x[2], reverse=True)
        return [
            {"id": doc_id, "text": text, "score": score}
            for doc_id, text, score in scores[:top_k]
        ]


def find_duplicates(
    texts: list[str], threshold: float = 0.92
) -> list[tuple[int, int, float]]:
    """Return pairs (index_a, index_b, score) above the similarity threshold."""
    embeddings = get_embeddings_batch(texts)
    matrix = cosine_similarity_matrix(embeddings)
    duplicates = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            if matrix[i][j] >= threshold:
                duplicates.append((i, j, float(matrix[i][j])))
    return duplicates
