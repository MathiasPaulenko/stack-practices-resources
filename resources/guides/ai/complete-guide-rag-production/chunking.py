"""Document chunking strategies from the RAG production guide.

Four strategies, cheapest first: fixed-size, sentence-based, semantic
(embedding-similarity breakpoints), and markdown-aware. Whichever you pick,
store source location metadata (file, page, section, chunk index) with each
chunk — citations and retrieval debugging depend on it.
"""
import math
import re
from typing import List


def fixed_size_chunks(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Split text into fixed-size character chunks with overlap.

    chunk_size/overlap are in characters here — for token-accurate
    boundaries, count tokens with tiktoken instead.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # overlap keeps straddling sentences recoverable

    return chunks


def sentence_chunks(text: str, max_chunk_size: int = 512) -> List[str]:
    """Pack whole sentences into chunks up to max_chunk_size characters."""
    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        candidate = f"{current_chunk} {sentence}".strip() if current_chunk else sentence
        if len(candidate) <= max_chunk_size:
            current_chunk = candidate
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def _cosine_similarity(a, b) -> float:
    """Cosine similarity for sequences of floats (lists or numpy arrays)."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def semantic_chunks(
    text: str,
    threshold: float = 0.8,
    model=None,
) -> List[str]:
    """Group consecutive sentences while cosine similarity stays above threshold.

    threshold is a heuristic: 0.8 works for most English prose with
    MiniLM embeddings, but tune it on your own documents — values between
    ~0.7 and ~0.9 are common depending on document density.

    model: any object with .encode(texts) -> embeddings (defaults to
    sentence-transformers all-MiniLM-L6-v2, downloaded on first use).
    Costs one embedding call per sentence — O(n) ingest overhead.
    """
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

    if len(sentences) <= 1:
        return sentences

    if model is None:
        # all-MiniLM-L6-v2 is a reasonable default; see sbert.net for alternatives
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings = model.encode(sentences)  # one embed call per sentence

    chunks = []
    current_chunk = [sentences[0]]

    for i in range(1, len(sentences)):
        sim = _cosine_similarity(embeddings[i], embeddings[i - 1])

        if sim > threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]

    chunks.append(" ".join(current_chunk))
    return chunks


def markdown_chunks(text: str, max_size: int = 512) -> List[str]:
    """Split markdown by headers; prepend header context to each chunk.

    Sections larger than max_size fall back to sentence-level splitting.
    """
    # (?P<header>...) captures keep header lines as split delimiters.
    # `\n?` also matches a header at the very start of the document.
    sections = re.split(r'(\n?#{1,6}\s+[^\n]+)', text)

    chunks = []
    current_section = ""
    current_header = ""

    for part in sections:
        if re.match(r'\n?#{1,6}\s+', part):
            if current_section.strip():
                section_text = (current_header + "\n" + current_section).strip()
                if len(section_text) > max_size:
                    chunks.extend(sentence_chunks(section_text, max_size))
                else:
                    chunks.append(section_text)
            current_header = part.strip()
            current_section = ""
        else:
            current_section += part

    if current_section.strip():
        chunks.append((current_header + "\n" + current_section).strip())

    return chunks


if __name__ == "__main__":
    doc = (
        "# Refund Policy\n"
        "Customers can request a refund within 30 days of purchase. "
        "The refund is issued to the original payment method. "
        "Digital products are non-refundable once downloaded.\n\n"
        "## Exceptions\n"
        "Subscriptions can be cancelled anytime; the current period "
        "remains active until the next billing date."
    )
    print("fixed :", len(fixed_size_chunks(doc, chunk_size=100, overlap=10)), "chunks")
    print("marker:", sentence_chunks(doc, max_chunk_size=120))
    print("md    :", markdown_chunks(doc, max_size=120))
