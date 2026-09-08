"""Semantic search with sentence-transformers and FAISS (local, free)."""
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class SemanticSearchFAISS:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents: list[str] = []

    def index_documents(self, documents: list[str]) -> None:
        self.documents = documents
        embeddings = self.model.encode(
            documents, convert_to_numpy=True, normalize_embeddings=True
        ).astype("float32")
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

    def search(self, query: str, k: int = 2) -> list[tuple[str, float]]:
        if self.index is None:
            raise RuntimeError("Index is empty. Call index_documents first.")
        q_emb = self.model.encode([query], normalize_embeddings=True).astype("float32")
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
    search = SemanticSearchFAISS()
    search.index_documents(docs)
    for doc, score in search.search("language for web development", k=2):
        print(f"{score:.3f}  {doc}")
