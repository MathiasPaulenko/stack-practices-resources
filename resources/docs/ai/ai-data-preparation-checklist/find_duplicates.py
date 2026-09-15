"""Exact and near-duplicate detection for document corpora."""

import hashlib
from typing import List, Dict


def find_exact_duplicates(documents: List[Dict]) -> Dict[str, str]:
    """Return a dict of doc_id -> original_id for exact content matches."""
    hashes = {}
    duplicates = {}
    for doc in documents:
        content_hash = hashlib.sha256(doc["content"].encode()).hexdigest()
        if content_hash in hashes:
            duplicates[doc["id"]] = hashes[content_hash]
        else:
            hashes[content_hash] = doc["id"]
    return duplicates


def find_near_duplicates(documents: List[Dict], threshold: float = 0.95) -> List[Dict]:
    """Return pairs of near-duplicate documents above the cosine similarity threshold."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([d["content"] for d in documents])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    np.fill_diagonal(similarity_matrix, 0)

    duplicates = []
    for i in range(len(documents)):
        for j in range(i + 1, len(documents)):
            if similarity_matrix[i][j] > threshold:
                duplicates.append({
                    "doc_a": documents[i]["id"],
                    "doc_b": documents[j]["id"],
                    "similarity": float(similarity_matrix[i][j]),
                })
    return duplicates


if __name__ == "__main__":
    docs = [
        {"id": "a", "content": "The quick brown fox jumps over the lazy dog."},
        {"id": "b", "content": "The quick brown fox jumps over the lazy dog."},
        {"id": "c", "content": "A completely different sentence about databases."},
    ]
    print("Exact duplicates:", find_exact_duplicates(docs))
    print("Near duplicates:", find_near_duplicates(docs, threshold=0.5))
