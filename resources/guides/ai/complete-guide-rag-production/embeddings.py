"""Embedding helpers: local sentence-transformers and OpenAI batch API.

Two ways to produce embeddings, same output shape (list of float vectors):

- local_embed(): free after setup, keeps data on-premise, CPU-friendly for
  batch ingest. You own model selection, versioning, and hardware.
- batch_embed(): OpenAI embeddings API with concurrent batches via
  asyncio.gather — real concurrency matters at scale; sequential awaits make
  ingest latency-bound on round-trips.

Never change the embedding model without re-embedding the entire corpus:
vectors from different models are not comparable.
"""
import asyncio
from typing import Any, List

DEFAULT_LOCAL_MODEL = "all-MiniLM-L6-v2"  # see sbert.net for alternatives
DEFAULT_OPENAI_MODEL = "text-embedding-3-small"  # check OpenAI docs for current models


def local_embed(
    texts: List[str],
    model_name: str = DEFAULT_LOCAL_MODEL,
    batch_size: int = 64,
) -> List[List[float]]:
    """Embed texts locally with sentence-transformers.

    Downloads the model on first use. For multilingual corpora, check the
    model's language coverage explicitly — English-tuned embeddings degrade
    badly on other languages.
    """
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=False)
    return embeddings.tolist()


async def embed_batch(client: Any, texts: List[str], model: str = DEFAULT_OPENAI_MODEL) -> List[List[float]]:
    """Single embeddings API call. client is an openai.AsyncOpenAI instance."""
    response = await client.embeddings.create(model=model, input=texts)
    # Sort by index so output order matches input order regardless of API ordering.
    return [d.embedding for d in sorted(response.data, key=lambda d: d.index)]


async def batch_embed(
    client: Any,
    texts: List[str],
    batch_size: int = 100,
    model: str = DEFAULT_OPENAI_MODEL,
) -> List[List[float]]:
    """Embed texts in batches with all batches in flight concurrently.

    Stay under the API's per-request input limits (check current docs —
    limits change). text-embedding-3-* also accepts a `dimensions` parameter
    to truncate output (Matryoshka) — validate retrieval quality at the
    reduced dimension before committing.
    """
    batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]
    results = await asyncio.gather(*(embed_batch(client, b, model=model) for b in batches))
    return [emb for batch in results for emb in batch]


if __name__ == "__main__":
    # Offline demo of batch_embed with a stub client — for real use pass
    # openai.AsyncOpenAI() (requires OPENAI_API_KEY).
    class _FakeEmbeddings:
        async def create(self, model, input):
            class _Data:
                def __init__(self, embedding, index):
                    self.embedding = embedding
                    self.index = index

            class _Response:
                pass

            response = _Response()
            response.data = [
                _Data([float(len(t))] * 8, i) for i, t in enumerate(input)
            ]
            return response

    class _FakeClient:
        embeddings = _FakeEmbeddings()

    chunks = ["chunk one text", "chunk two text", "chunk three text"]
    vectors = asyncio.run(batch_embed(_FakeClient(), chunks, batch_size=2))
    print(f"{len(vectors)} embeddings of dim {len(vectors[0])}")
    # Real local usage:
    #   vectors = local_embed(chunks)  # downloads model on first run
