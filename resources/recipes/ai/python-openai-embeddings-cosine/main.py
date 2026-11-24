"""Demo: compare texts and run a small similarity search.

Requires OPENAI_API_KEY in the environment.
"""

from similarity_search import (
    SimilaritySearchIndex,
    cosine_similarity,
    cosine_similarity_matrix,
    find_duplicates,
    get_embedding,
    get_embeddings_batch,
)


def compare_two_texts() -> None:
    text_a = "Redis is an in-memory data structure store used for caching."
    text_b = "Redis works as a fast cache by keeping data in memory."
    text_c = "PostgreSQL is a relational database with ACID compliance."

    emb_a = get_embedding(text_a)
    emb_b = get_embedding(text_b)
    emb_c = get_embedding(text_c)

    print(f"Similarity (a, b): {cosine_similarity(emb_a, emb_b):.4f}  # same topic")
    print(f"Similarity (a, c): {cosine_similarity(emb_a, emb_c):.4f}  # different")


def search_index_demo() -> None:
    index = SimilaritySearchIndex()
    index.add_batch(
        [
            ("doc1", "Redis is an in-memory data structure store for caching."),
            ("doc2", "PostgreSQL is a capable open-source relational database."),
            ("doc3", "Docker containers package applications with dependencies."),
            ("doc4", "Memcached is a distributed memory caching system."),
            ("doc5", "Kubernetes orchestrates containerized applications."),
        ]
    )
    for r in index.search("caching solution for fast lookups", top_k=3):
        print(f"Score: {r['score']:.4f} | {r['text'][:60]}")


def matrix_demo() -> None:
    texts = [
        "Redis caching strategies",
        "In-memory cache with Redis",
        "PostgreSQL database indexing",
        "Docker container deployment",
    ]
    matrix = cosine_similarity_matrix(get_embeddings_batch(texts))
    print(" " * 8, end="")
    for i in range(len(texts)):
        print(f" doc{i:>3d}", end="")
    print()
    for i, row in enumerate(matrix):
        print(f"doc{i:<4d}", end="")
        for val in row:
            print(f" {val:6.2f}", end="")
        print()


def dedup_demo() -> None:
    dups = find_duplicates(
        [
            "Redis is a fast in-memory cache.",
            "Redis works as an in-memory caching store.",
            "PostgreSQL is a relational database.",
        ]
    )
    print("Duplicates:", dups)


if __name__ == "__main__":
    compare_two_texts()
    print()
    search_index_demo()
    print()
    matrix_demo()
    print()
    dedup_demo()
