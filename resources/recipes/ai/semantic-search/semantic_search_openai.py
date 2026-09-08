"""Semantic search with OpenAI embeddings and FAISS."""
import os
import faiss
import numpy as np
from openai import OpenAI


class SemanticSearchOpenAI:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model
        self.index = None
        self.documents: list[str] = []

    def _embed(self, text: str) -> np.ndarray:
        resp = self.client.embeddings.create(input=text, model=self.model)
        return np.array(resp.data[0].embedding, dtype="float32")

    def index_documents(self, documents: list[str]) -> None:
        self.documents = documents
        embeddings = np.array([self._embed(d) for d in documents], dtype="float32")
        faiss.normalize_L2(embeddings)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

    def search(self, query: str, k: int = 2) -> list[tuple[str, float]]:
        if self.index is None:
            raise RuntimeError("Index is empty. Call index_documents first.")
        q_emb = self._embed(query).reshape(1, -1)
        faiss.normalize_L2(q_emb)
        distances, indices = self.index.search(q_emb, k)
        return [
            (self.documents[idx], float(distances[0][rank]))
            for rank, idx in enumerate(indices[0])
        ]


if __name__ == "__main__":
    docs = [
        "Python is great for data science and machine learning.",
        "JavaScript runs in browsers and on servers via Node.js.",
        "Rust offers memory safety without a garbage collector.",
    ]
    search = SemanticSearchOpenAI()
    search.index_documents(docs)
    for doc, score in search.search("language for web development", k=2):
        print(f"{score:.3f}  {doc}")
