"""Query the RAG pipeline: embed question, retrieve chunks, answer with citations.

Usage:
    export OPENAI_API_KEY=sk-...
    python query.py "How do vector indexes work?"
"""
import sys

import psycopg2
from openai import OpenAI
from pgvector.psycopg2 import register_vector

client = OpenAI()
conn = psycopg2.connect("dbname=ragdb user=rag password=rag host=localhost")
register_vector(conn)


def embed_text(text: str) -> list[float]:
    resp = client.embeddings.create(input=text, model="text-embedding-3-small")
    return resp.data[0].embedding


def rag_query(question: str, top_k: int = 5) -> str:
    q_emb = embed_text(question)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT content, doc_id, chunk_index, "
            "1 - (embedding <=> %s) AS similarity "
            "FROM doc_chunks "
            "ORDER BY embedding <=> %s "
            "LIMIT %s",
            (q_emb, q_emb, top_k),
        )
        results = cur.fetchall()

    context = "\n\n".join(r[0] for r in results)
    sources = [f"doc:{r[1]} chunk:{r[2]} sim:{r[3]:.3f}" for r in results]
    prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        f"Answer based on the context. Cite the source."
    )
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content + "\n\nSources: " + ", ".join(sources)


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How do vector indexes work?"
    print(rag_query(question))
