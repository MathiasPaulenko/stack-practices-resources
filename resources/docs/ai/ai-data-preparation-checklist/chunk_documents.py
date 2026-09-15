"""Document chunking for RAG pipelines using LangChain's RecursiveCharacterTextSplitter."""

from typing import List, Dict


def chunk_documents(
    documents: List[Dict],
    chunk_size: int = 512,
    overlap: int = 50,
) -> List[Dict]:
    """Split documents into chunks with metadata attached."""
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = []
    for doc in documents:
        doc_chunks = splitter.split_text(doc["content"])
        for i, chunk in enumerate(doc_chunks):
            chunks.append({
                "id": f"{doc['id']}_chunk_{i}",
                "content": chunk,
                "metadata": {
                    "source": doc.get("source", "unknown"),
                    "title": doc.get("title", "untitled"),
                    "chunk_index": i,
                    "total_chunks": len(doc_chunks),
                },
            })
    return chunks


if __name__ == "__main__":
    docs = [
        {"id": "doc1", "content": "This is a sample document. " * 50, "source": "test", "title": "Sample"},
    ]
    result = chunk_documents(docs, chunk_size=100, overlap=20)
    print(f"Generated {len(result)} chunks")
    for c in result[:2]:
        print(f"  {c['id']}: {len(c['content'])} chars")
