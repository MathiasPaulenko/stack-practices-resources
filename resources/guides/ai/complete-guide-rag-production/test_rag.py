"""Offline unit tests — no API keys, no model downloads. Run: pytest test_rag.py -v"""
import asyncio

from chunking import (
    fixed_size_chunks,
    markdown_chunks,
    semantic_chunks,
    sentence_chunks,
)
from context_assembly import assemble_context, build_rag_prompt
from hybrid_search import (
    HybridSearch,
    SimpleKeywordIndex,
    reciprocal_rank_fusion,
)
from rag_pipeline import RAGPipeline
from rerankers import _ranked, cohere_rerank
from vector_stores import PgVectorStore, _chroma_shaped


# ---------- chunking ----------

def test_fixed_size_chunks_overlap_and_coverage():
    text = "abcdefghij" * 30  # 300 chars
    chunks = fixed_size_chunks(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(len(c) <= 100 for c in chunks)
    # Overlap means consecutive chunks share a suffix/prefix.
    assert chunks[0][-20:] == chunks[1][:20]
    # Reconstruct coverage: first chunk starts at 0.
    assert chunks[0] == text[:100]


def test_sentence_chunks_respect_boundaries():
    text = "First sentence here. Second one is a bit longer than the first. Third!"
    chunks = sentence_chunks(text, max_chunk_size=45)
    assert len(chunks) >= 2
    # No chunk should cut a sentence mid-way: every chunk ends at sentence end.
    for c in chunks:
        assert c.rstrip().endswith((".", "!", "?"))
    assert " ".join(chunks).count("First sentence") == 1


def test_markdown_chunks_prepends_header_context():
    text = (
        "# Refund Policy\n"
        "Refunds are issued within 30 days. Digital products are excluded.\n\n"
        "## Exceptions\n"
        "Subscriptions cancel anytime."
    )
    chunks = markdown_chunks(text, max_size=1000)
    assert len(chunks) == 2
    assert chunks[0].startswith("# Refund Policy")
    assert chunks[1].startswith("## Exceptions")
    assert "Subscriptions cancel anytime" in chunks[1]


def test_semantic_chunks_breaks_on_topic_shift():
    class _FakeModel:
        """3 sentences: first two similar, third dissimilar."""

        def encode(self, texts):
            return [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]][:len(texts)]

    text = "Cats are great pets. Dogs are also wonderful companions. Pizza is Italian food."
    chunks = semantic_chunks(text, threshold=0.8, model=_FakeModel())
    assert len(chunks) == 2
    assert "Cats" in chunks[0] and "Dogs" in chunks[0]
    assert "Pizza" in chunks[1]


# ---------- context assembly ----------

class _WordEncoding:
    """Whitespace tokenizer stand-in for tiktoken — token == word."""

    def encode(self, text):
        return text.split()

    def decode(self, tokens):
        return " ".join(tokens)


def test_assemble_context_respects_token_budget():
    docs = [
        {"text": "word " * 20, "metadata": {"source": "a.pdf"}},
        {"text": "word " * 20, "metadata": {"source": "b.pdf"}},
        {"text": "word " * 20, "metadata": {"source": "c.pdf"}},
    ]
    context = assemble_context(docs, max_context_tokens=55, encoding=_WordEncoding())
    # Two 20-token docs fit (40 <= 55); the third is dropped entirely.
    assert "[Source 1]" in context and "[Source 2]" in context
    assert "[Source 3]" not in context
    assert "(Source: a.pdf)" in context


def test_assemble_context_truncates_when_slice_fits():
    docs = [
        {"text": "short doc", "metadata": {"source": "a.pdf"}},
        {"text": "filler " * 200, "metadata": {"source": "b.pdf"}},
    ]
    context = assemble_context(docs, max_context_tokens=150, encoding=_WordEncoding())
    # ~8 tokens used; remaining ~142 > 100 -> truncated slice appended.
    assert "[Source 2]:" in context and context.rstrip().endswith("...")


def test_build_rag_prompt_structure():
    messages = build_rag_prompt("What is RAG?", "[Source 1]: context text")
    assert [m["role"] for m in messages] == ["system", "user"]
    assert "context text" in messages[1]["content"]
    assert "What is RAG?" in messages[1]["content"]
    assert "don't know" in messages[0]["content"]


# ---------- hybrid search ----------

class _FakeVectorStore:
    def __init__(self, ids, texts, distances):
        self._result = {
            "ids": [ids],
            "documents": [texts],
            "metadatas": [[{"source": "s"} for _ in ids]],
            "distances": [distances],
        }

    def query(self, query_embeddings, n_results=10, where=None):
        return self._result


def test_hybrid_search_merges_vector_and_keyword():
    store = _FakeVectorStore(
        ids=["d1", "d2"],
        texts=["vector doc one", "vector doc two"],
        distances=[0.1, 0.5],
    )
    index = SimpleKeywordIndex()
    index.add("d2", "keyword match in doc two", {"source": "s"})
    index.add("d3", "keyword only doc three", {"source": "s"})

    hybrid = HybridSearch(store, index, alpha=0.5)
    results = hybrid.search("keyword match", query_embedding=[0.0] * 4, top_k=5)
    ids = [r["id"] for r in results]
    # d2 appears in both retrievers; d3 is keyword-only and must be included.
    assert "d2" in ids and "d3" in ids and "d1" in ids
    # d2 should outrank d3 (present in both signals).
    assert ids.index("d2") < ids.index("d3")


def test_hybrid_search_alpha_zero_is_keyword_only_boost():
    store = _FakeVectorStore(ids=["v1"], texts=["vec"], distances=[0.0])
    index = SimpleKeywordIndex()
    index.add("k1", "alpha test keyword", {})

    hybrid = HybridSearch(store, index, alpha=0.0)
    results = hybrid.search("alpha test", query_embedding=[0.0], top_k=5)
    # Vector contribution is zeroed; keyword doc still ranks.
    assert results[0]["id"] == "k1"


def test_reciprocal_rank_fusion_prefers_consensus():
    fused = reciprocal_rank_fusion([["a", "b", "c"], ["b", "a", "d"]])
    assert fused[0][0] in {"a", "b"}
    # Items appearing in both lists outrank single-list items.
    assert dict(fused)["c"] < dict(fused)["a"]
    assert dict(fused)["d"] < dict(fused)["b"]


def test_pgvector_rejects_bad_table_name():
    import pytest

    with pytest.raises(ValueError):
        PgVectorStore("postgresql://localhost/db", table="docs; DROP TABLE x")


def test_chroma_shaped_result():
    res = _chroma_shaped(["1"], ["text"], [{"s": 1}], [0.2])
    assert res == {
        "ids": [["1"]],
        "documents": [["text"]],
        "metadatas": [[{"s": 1}]],
        "distances": [[0.2]],
    }


# ---------- rerankers ----------

def test_ranked_sorts_by_score_desc():
    out = _ranked(["low", "high", "mid"], [0.1, 0.9, 0.5], top_k=2)
    assert [r["text"] for r in out] == ["high", "mid"]
    assert out[0]["score"] == 0.9


def test_cohere_rerank_maps_results():
    class _Result:
        def __init__(self, index, score):
            self.index = index
            self.relevance_score = score

    class _Response:
        results = [_Result(1, 0.9), _Result(0, 0.4)]

    class _FakeClient:
        def rerank(self, model, query, documents, top_n):
            assert top_n == 2
            return _Response()

    out = cohere_rerank("q", ["doc zero", "doc one"], top_k=2, client=_FakeClient())
    assert out[0]["text"] == "doc one" and out[0]["score"] == 0.9
    assert out[1]["index"] == 0


# ---------- full pipeline (stubbed models) ----------

def test_rag_pipeline_answer_end_to_end():
    class _HashEmbedder:
        def encode(self, text):
            # Deterministic: 'refund' docs share a dimension.
            vec = [0.0] * 8
            vec[0 if "refund" in text.lower() else 1] = 1.0
            return vec

    class _Collection:
        def __init__(self):
            self.docs = [
                {"text": "refunds within 30 days", "metadata": {"source": "a"}},
                {"text": "unrelated weather note", "metadata": {"source": "b"}},
            ]

        def query(self, query_embeddings, n_results=10, where=None):
            qe = query_embeddings[0]
            def dot(d):
                return sum(x * y for x, y in zip(qe, d["embedding"]))
            ranked = sorted(
                [{"text": d["text"], "metadata": d["metadata"],
                  "embedding": _HashEmbedder().encode(d["text"])} for d in self.docs],
                key=lambda d: -dot(d),
            )[:n_results]
            return {
                "ids": [[f"id{i}" for i in range(len(ranked))]],
                "documents": [[d["text"] for d in ranked]],
                "metadatas": [[d["metadata"] for d in ranked]],
                "distances": [[1.0 - dot(d) for d in ranked]],
            }

    class _Reranker:
        def predict(self, pairs):
            return [1.0 if "refund" in d.lower() else 0.0 for _, d in pairs]

    class _Completions:
        async def create(self, model, messages, temperature):
            class _M:
                content = "stub answer"
            class _C:
                message = _M()
            class _R:
                choices = [_C()]
            return _R()

    class _LLM:
        class _Chat:
            completions = _Completions()
        chat = _Chat()

    rag = RAGPipeline(
        _Collection(),
        embedder=_HashEmbedder(),
        reranker=_Reranker(),
        llm_client=_LLM(),
    )
    result = asyncio.run(rag.answer("refund policy?", top_k=2))
    assert result["answer"] == "stub answer"
    assert result["retrieved_count"] == 2
    assert result["sources"][0]["source"] in {"a", "b"}
