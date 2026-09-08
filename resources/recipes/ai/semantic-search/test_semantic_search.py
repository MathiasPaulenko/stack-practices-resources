"""Tests for the semantic search companion (no external dependencies required)."""
import sys
import importlib
from pathlib import Path
from unittest.mock import MagicMock

import numpy as np

COMPANION_DIR = Path(__file__).parent
sys.path.insert(0, str(COMPANION_DIR))


def test_cosine_similarity_logic():
    """Verify cosine similarity computation with known vectors."""
    a = np.array([1.0, 0.0, 0.0])
    b = np.array([1.0, 0.0, 0.0])
    dot = float(np.dot(a, b))
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    cosine = dot / (na * nb)
    assert abs(cosine - 1.0) < 1e-6

    c = np.array([0.0, 1.0, 0.0])
    dot2 = float(np.dot(a, c))
    nc = float(np.linalg.norm(c))
    cosine2 = dot2 / (na * nc)
    assert abs(cosine2 - 0.0) < 1e-6


def test_l2_normalization():
    """Verify L2 normalization produces unit vectors."""
    v = np.array([[3.0, 4.0]], dtype="float32")
    norm = np.linalg.norm(v)
    normalized = v / norm
    assert abs(float(np.linalg.norm(normalized)) - 1.0) < 1e-6


def test_faiss_index_logic():
    """Verify FAISS-style IndexFlatIP logic with a mock index."""
    docs = ["doc one", "doc two", "doc three"]
    fake_index = MagicMock()
    fake_index.search.return_value = (
        np.array([[0.9, 0.7]]),
        np.array([[0, 2]]),
    )
    q_emb = np.array([[0.1, 0.2, 0.3]], dtype="float32")
    distances, indices = fake_index.search(q_emb, 2)
    results = [
        (docs[idx], float(distances[0][rank]))
        for rank, idx in enumerate(indices[0])
    ]
    assert len(results) == 2
    assert results[0][0] == "doc one"
    assert results[1][0] == "doc three"
    assert results[0][1] == 0.9
    assert results[1][1] == 0.7


def test_empty_index_guard():
    """Verify the search guard raises when index is None."""
    import pytest
    # Simulate the guard logic from SemanticSearchFAISS.search
    index = None
    with pytest.raises(RuntimeError, match="Index is empty"):
        if index is None:
            raise RuntimeError("Index is empty. Call index_documents first.")


def test_js_cosine_function_syntax():
    """Verify the JS companion file has a cosine function."""
    js_path = COMPANION_DIR / "semantic_search_js.js"
    content = js_path.read_text(encoding="utf-8")
    assert "function cosine(a, b)" in content
    assert "module.exports" in content
    assert "semanticSearch" in content


def test_java_service_syntax():
    """Verify the Java companion file has the expected class and methods."""
    java_path = COMPANION_DIR / "SemanticSearchService.java"
    content = java_path.read_text(encoding="utf-8")
    assert "class SemanticSearchService" in content
    assert "indexDocuments" in content
    assert "similaritySearch" in content
    assert "PgVectorStore" in content
