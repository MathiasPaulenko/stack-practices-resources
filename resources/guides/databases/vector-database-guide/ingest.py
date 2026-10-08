"""Ingest documents into pgvector as embedded chunks.

Usage:
    export OPENAI_API_KEY=sk-...
    python ingest.py docs/           # directory of .txt/.md files
"""
import sys
from pathlib import Path

import psycopg2
from openai import OpenAI
from pgvector.psycopg2 import register_vector

CHUNK_SIZE = 500   # ~500 tokens ≈ 2000 chars; adjust per corpus
OVERLAP = 50       # ~10% overlap keeps context across chunk boundaries

client = OpenAI()
conn = psycopg2.connect("dbname=ragdb user=rag password=rag host=localhost")
register_vector(conn)


def chunk_text(text: str, size: int = CHUNK_SIZE * 4, overlap: int = OVERLAP * 4) -> list[str]:
    """Split text into overlapping character windows."""
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return [c.strip() for c in chunks if c.strip()]


def embed_text(text: str) -> list[float]:
    resp = client.embeddings.create(input=text, model="text-embedding-3-small")
    return resp.data[0].embedding


def ingest_document(doc_id: str, chunks: list[str]):
    for i, chunk in enumerate(chunks):
        emb = embed_text(chunk)
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO doc_chunks (doc_id, chunk_index, content, embedding) "
                "VALUES (%s, %s, %s, %s)",
                (doc_id, i, chunk, emb),
            )
    conn.commit()
    print(f"{doc_id}: {len(chunks)} chunks ingested")


if __name__ == "__main__":
    docs_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    for path in sorted(docs_dir.glob("**/*.txt")) + sorted(docs_dir.glob("**/*.md")):
        ingest_document(path.stem, chunk_text(path.read_text(encoding="utf-8")))
