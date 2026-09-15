"""Generate embeddings for document chunks using OpenAI's API."""

from typing import List, Dict
import time


def generate_embeddings(
    chunks: List[Dict],
    model: str = "text-embedding-3-small",
    batch_size: int = 100,
) -> List[Dict]:
    """Embed chunks in batches with rate limiting."""
    from openai import OpenAI

    client = OpenAI()
    embeddings = []

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["content"] for c in batch]

        response = client.embeddings.create(model=model, input=texts)

        for j, embedding in enumerate(response.data):
            embeddings.append({
                "chunk_id": batch[j]["id"],
                "embedding": embedding.embedding,
                "content": batch[j]["content"],
                "metadata": batch[j].get("metadata", {}),
            })

        time.sleep(0.5)

    return embeddings


if __name__ == "__main__":
    print("Set OPENAI_API_KEY and provide chunks to run this script.")
