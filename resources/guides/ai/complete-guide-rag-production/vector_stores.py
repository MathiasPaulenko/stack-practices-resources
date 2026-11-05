"""Vector store adapters: Chroma, Pinecone, and pgvector.

All three classes expose the same minimal interface so they can be swapped
without touching retrieval code:

    store.add(ids=..., documents=..., embeddings=..., metadatas=...)
    store.query(query_embeddings=[vec], n_results=10, where={...})
        -> {"ids": [[...]], "documents": [[...]],
            "metadatas": [[...]], "distances": [[...]]}

The query result is Chroma-shaped on purpose: distances are "lower = more
similar" (cosine distance) for every store, so hybrid search and reranking
code works against any of them.

The store returns candidates, not answers — start with top_k around 20-50
and let reranking cut to 5.
"""
import os
import re
from typing import Any, Dict, List, Optional

_TABLE_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


def _chroma_shaped(ids, documents, metadatas, distances) -> Dict[str, list]:
    """Normalize a flat result list into the Chroma query-result shape."""
    return {
        "ids": [ids],
        "documents": [documents],
        "metadatas": [metadatas],
        "distances": [distances],
    }


class ChromaStore:
    """ChromaDB — embedded library / self-hosted.

    Fastest way to a working prototype; runs in-process and persists to
    disk. Not built for multi-tenant production; durability is your problem.
    """

    def __init__(self, path: str = "./vector_db", collection_name: str = "documents",
                 distance_metric: str = "cosine"):
        import chromadb

        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": distance_metric},
        )

    def add(self, ids: List[str], documents: List[str],
            embeddings: List[List[float]], metadatas: List[Dict[str, Any]]) -> None:
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(self, query_embeddings: List[List[float]], n_results: int = 10,
              where: Optional[Dict[str, Any]] = None) -> Dict[str, list]:
        kwargs: Dict[str, Any] = {"query_embeddings": query_embeddings, "n_results": n_results}
        if where:
            kwargs["where"] = where  # e.g. {"source": "file1.pdf"}
        return self.collection.query(**kwargs)


class PineconeStore:
    """Pinecone — fully managed, serverless.

    Removes all index operations but bills per vector and per query.
    Dimension and metric are fixed at index creation time.
    """

    def __init__(self, index_name: str = "documents", dimension: int = 1536,
                 api_key: Optional[str] = None, cloud: str = "aws",
                 region: str = "us-east-1"):
        from pinecone import Pinecone, ServerlessSpec

        self.pc = Pinecone(api_key=api_key or os.environ["PINECONE_API_KEY"])

        # Create the index once if missing — check latest docs for current API.
        existing = {idx.name for idx in self.pc.list_indexes()}
        if index_name not in existing:
            self.pc.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud=cloud, region=region),
            )

        self.index = self.pc.Index(index_name)

    def add(self, ids: List[str], documents: List[str],
            embeddings: List[List[float]], metadatas: List[Dict[str, Any]]) -> None:
        vectors = [
            {
                "id": doc_id,
                "values": emb,
                "metadata": {**meta, "text": doc},
            }
            for doc_id, doc, emb, meta in zip(ids, documents, embeddings, metadatas)
        ]
        self.index.upsert(vectors=vectors)

    def query(self, query_embeddings: List[List[float]], n_results: int = 10,
              where: Optional[Dict[str, Any]] = None) -> Dict[str, list]:
        kwargs: Dict[str, Any] = {
            "vector": query_embeddings[0],
            "top_k": n_results,
            "include_metadata": True,
        }
        if where:
            kwargs["filter"] = where  # e.g. {"source": {"$eq": "file_1.pdf"}}

        matches = self.index.query(**kwargs)["matches"]

        ids, docs, metas, distances = [], [], [], []
        for m in matches:
            meta = dict(m.get("metadata") or {})
            docs.append(meta.pop("text", ""))
            ids.append(m["id"])
            metas.append(meta)
            # Pinecone cosine score is similarity; convert to distance.
            distances.append(1.0 - m["score"])

        return _chroma_shaped(ids, docs, metas, distances)


class PgVectorStore:
    """pgvector — vectors inside Postgres next to your metadata.

    Right call when the corpus is modest and you already run Postgres.
    Uses psycopg3 (not psycopg2) — register_vector adapts vectors for it.
    """

    def __init__(self, conninfo: str, table: str = "documents",
                 embedding_dim: int = 1536):
        if not _TABLE_RE.match(table):
            raise ValueError(f"Invalid table name: {table!r}")
        self.table = table

        import psycopg
        from pgvector.psycopg import register_vector

        self.conn = psycopg.connect(conninfo)
        register_vector(self.conn)
        self._ensure_table(embedding_dim)

    def _ensure_table(self, dim: int) -> None:
        with self.conn.cursor() as cur:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    embedding vector({dim}),
                    metadata jsonb
                )
            """)
            # HNSW index: m and ef_construction trade build cost vs recall.
            cur.execute(f"""
                CREATE INDEX IF NOT EXISTS {self.table}_embedding_idx
                ON {self.table} USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64)
            """)
        self.conn.commit()

    def add(self, ids: List[str], documents: List[str],
            embeddings: List[List[float]], metadatas: List[Dict[str, Any]]) -> None:
        # ids are ignored: the table uses a SERIAL primary key. Keep them in
        # metadata if you need stable external identifiers.
        from psycopg.types.json import Json

        with self.conn.cursor() as cur:
            for doc, emb, meta in zip(documents, embeddings, metadatas):
                cur.execute(
                    f"INSERT INTO {self.table} (content, embedding, metadata) VALUES (%s, %s, %s)",
                    (doc, emb, Json(meta)),
                )
        self.conn.commit()

    def query(self, query_embeddings: List[List[float]], n_results: int = 10,
              where: Optional[Dict[str, Any]] = None) -> Dict[str, list]:
        # <=> is cosine distance (lower = more similar).
        sql = f"SELECT id, content, metadata, embedding <=> %s AS distance FROM {self.table}"
        params: List[Any] = [query_embeddings[0]]

        # where supports simple metadata equality filters only, e.g.
        # {"source": "file1.pdf"} -> metadata->>'source' = 'file1.pdf'
        clauses = []
        for key, value in (where or {}).items():
            clauses.append("metadata ->> %s = %s")
            params.extend([key, str(value)])
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)

        sql += " ORDER BY embedding <=> %s LIMIT %s"
        params.extend([query_embeddings[0], n_results])

        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        return _chroma_shaped(
            ids=[str(r[0]) for r in rows],
            documents=[r[1] for r in rows],
            metadatas=[r[2] or {} for r in rows],
            distances=[float(r[3]) for r in rows],
        )


if __name__ == "__main__":
    # Offline demo with Chroma only — Pinecone and pgvector need
    # credentials / a running Postgres with the vector extension.
    import tempfile

    try:
        import chromadb  # noqa: F401 — ChromaStore imports it lazily too
    except ImportError:
        raise SystemExit("pip install chromadb to run this demo")

    docs = [
        "Paris is the capital of France.",
        "Berlin is the capital of Germany.",
        "Tokyo is the capital of Japan.",
    ]
    # Toy embeddings: one-hot-ish vectors so "capital" queries behave sanely.
    vocab = {"paris": 0, "berlin": 1, "tokyo": 2, "capital": 3, "france": 4,
             "germany": 5, "japan": 6}

    def toy_embed(text: str) -> List[float]:
        vec = [0.0] * len(vocab)
        for tok in text.lower().split():
            if tok in vocab:
                vec[vocab[tok]] = 1.0
        return vec

    store = ChromaStore(path=tempfile.mkdtemp())
    store.add(
        ids=[f"doc_{i}" for i in range(len(docs))],
        documents=docs,
        embeddings=[toy_embed(d) for d in docs],
        metadatas=[{"source": "geo.txt", "chunk_index": i} for i in range(len(docs))],
    )
    res = store.query(query_embeddings=[toy_embed("capital of Germany")], n_results=2)
    for doc, dist in zip(res["documents"][0], res["distances"][0]):
        print(f"distance={dist:.3f}  {doc}")
