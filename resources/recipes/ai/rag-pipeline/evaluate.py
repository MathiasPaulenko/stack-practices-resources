"""Minimal retrieval evaluation: check whether the right chunks land in top-k.

Runs a small question set against the persisted Chroma store and reports
retrieval hit rate. Extend `TEST_SET` with questions whose expected source
passage is known.

    python evaluate.py
"""

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from rag_pipeline import COLLECTION, PERSIST_DIR

# (question, substring that must appear in at least one retrieved chunk)
TEST_SET = [
    ("What is the refund policy?", "30 days"),
    ("How long is the warranty?", "12 months"),
    ("Do you ship internationally?", "shipping"),
]


def main() -> None:
    store = Chroma(
        collection_name=COLLECTION,
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
        persist_directory=PERSIST_DIR,
    )
    retriever = store.as_retriever(search_kwargs={"k": 4})

    hits = 0
    for question, expected in TEST_SET:
        chunks = retriever.invoke(question)
        hit = any(expected.lower() in c.page_content.lower() for c in chunks)
        hits += hit
        status = "HIT " if hit else "MISS"
        print(f"{status} {question}")

    total = len(TEST_SET)
    print(f"\nRetrieval hit rate: {hits}/{total} ({hits / total:.0%})")


if __name__ == "__main__":
    main()
