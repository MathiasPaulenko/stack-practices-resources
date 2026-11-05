"""Context assembly: fit reranked chunks into the prompt's token budget.

Before the LLM call, retrieved chunks become a prompt — and the prompt has
a hard token ceiling shared with system instructions, conversation history,
and the answer's output budget. Most production RAG systems land between
2k and 8k tokens of context, tuned per use case.

Two decisions matter:

- How much context: more retrieved text helps recall but dilutes attention
  and inflates cost.
- How to truncate: prefer dropping whole lower-ranked chunks over slicing
  text — partial chunks confuse the model more than they help. When you
  must slice, truncate on token boundaries (tiktoken with the target
  model's encoding), not character counts — len(text) // 4 drifts badly on
  code, non-English text, and emoji.

Keep [Source N] markers: they cost a few tokens and buy citations plus
debuggability (trace a wrong answer back to a specific retrieved chunk).
"""
from typing import Any, Dict, List, Optional

_ENCODING = None


def _get_encoding():
    """tiktoken encoding for the model consuming the context (lazy import)."""
    global _ENCODING
    if _ENCODING is None:
        import tiktoken

        # Match the tokenizer of the model that will consume the context.
        _ENCODING = tiktoken.encoding_for_model("gpt-4o")
    return _ENCODING


def assemble_context(
    retrieved_docs: List[Dict[str, Any]],
    max_context_tokens: int = 4000,
    include_metadata: bool = True,
    encoding: Any = None,
) -> str:
    """Assemble retrieved chunks into a token-budgeted context string.

    retrieved_docs: list of {"text": str, "metadata": {...}} dicts, ordered
    by relevance (reranked). encoding: optional tiktoken Encoding override —
    pass one in tests to avoid the model download.
    """
    encoding = encoding or _get_encoding()

    context_parts = []
    current_tokens = 0

    for i, doc in enumerate(retrieved_docs):
        doc_tokens = len(encoding.encode(doc["text"]))

        if current_tokens + doc_tokens > max_context_tokens:
            # Drop the chunk entirely unless a meaningful slice still fits —
            # partial chunks tend to confuse the model more than they help.
            remaining = max_context_tokens - current_tokens
            if remaining > 100:
                truncated = encoding.decode(encoding.encode(doc["text"])[:remaining])
                context_parts.append(f"[Source {i + 1}]: {truncated} ...")
            break

        source_info = ""
        if include_metadata and "metadata" in doc:
            meta = doc["metadata"]
            source_info = f" (Source: {meta.get('source', 'unknown')})"

        context_parts.append(f"[Source {i + 1}]{source_info}: {doc['text']}")
        current_tokens += doc_tokens

    return "\n\n".join(context_parts)


def build_rag_prompt(query: str, context: str) -> List[Dict[str, str]]:
    """Wrap context + question into chat messages for the LLM call."""
    return [
        {
            "role": "system",
            "content": (
                "Answer the user's question based on the provided context. "
                "If the context doesn't contain relevant information, say you don't know. "
                "Cite the source number for every claim drawn from the context."
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}",
        },
    ]


if __name__ == "__main__":
    # Offline demo with a whitespace "encoding" — no tiktoken download.
    class _WordEncoding:
        def encode(self, text: str) -> List[str]:
            return text.split()

        def decode(self, tokens: List[str]) -> str:
            return " ".join(tokens)

    docs = [
        {"text": "Refunds are processed within 5 business days.", "metadata": {"source": "billing.pdf"}},
        {"text": "SSO setup lives under Admin > Security > Identity providers.", "metadata": {"source": "admin.pdf"}},
        {"text": " " * 10 + "filler " * 200, "metadata": {"source": "big.pdf"}},
    ]
    context = assemble_context(docs, max_context_tokens=60, encoding=_WordEncoding())
    print(context)
    print("---")
    for msg in build_rag_prompt("How do refunds work?", context):
        print(f"[{msg['role']}] {msg['content'][:80]}")
