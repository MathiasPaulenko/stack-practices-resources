"""Minimal RAG grounding: embed corpus once, embed query at runtime.

The naive version re-embeds every document per request — do NOT do that
in production. Requires OPENAI_API_KEY and numpy.
"""
import numpy as np
from openai import OpenAI

client = OpenAI()


def get_embedding(text: str) -> list[float]:
    return client.embeddings.create(
        model="text-embedding-3-small", input=text
    ).data[0].embedding


def build_index(documents: list[str]) -> list[tuple[str, list[float]]]:
    """Run at indexing time — once, not per request."""
    return [(doc, get_embedding(doc)) for doc in documents]


def retrieve(index: list[tuple[str, list[float]]], query: str, top_k: int = 3) -> list[str]:
    q = get_embedding(query)
    scored = sorted(
        index,
        key=lambda d: np.dot(q, d[1]) / (np.linalg.norm(q) * np.linalg.norm(d[1])),
        reverse=True,
    )
    return [doc for doc, _ in scored[:top_k]]


def rag_answer(index, query: str) -> str:
    context = retrieve(index, query)
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer using only the provided context. "
                    "If the context does n
