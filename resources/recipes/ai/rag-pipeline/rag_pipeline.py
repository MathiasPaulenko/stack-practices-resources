"""Runnable RAG pipeline: chunk -> embed -> store -> retrieve -> generate.

Uses current LangChain packages (langchain-openai, langchain-chroma,
langchain-community). Set OPENAI_API_KEY before running:

    pip install -r requirements.txt
    python rag_pipeline.py
"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

PERSIST_DIR = "./chroma_db"
COLLECTION = "knowledge_base"


def ingest(path: str = "knowledge_base.txt") -> Chroma:
    """Load, chunk, embed, and persist documents into Chroma."""
    docs = TextLoader(path).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma.from_documents(
        chunks,
        embeddings,
        collection_name=COLLECTION,
        persist_directory=PERSIST_DIR,
    )


def build_chain(vectorstore: Chroma):
    """Wire the retriever and LLM into a retrieval chain with a fallback prompt."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Answer using only this context. If the answer isn't in the "
        "context, say you don't know.\n\nContext:\n{context}\n\n"
        "Question: {input}"
    )
    return create_retrieval_chain(
        vectorstore.as_retriever(search_kwargs={"k": 4}),
        create_stuff_documents_chain(llm, prompt),
    )


def ask(chain, question: str) -> None:
    result = chain.invoke({"input": question})
    print(f"\nQ: {question}\nA: {result['answer']}\n")
    for doc in result["context"]:
        print(f"  source: {doc.metadata.get('source')}")


if __name__ == "__main__":
    store = ingest()
    qa = build_chain(store)
    ask(qa, "What is the refund policy?")
    ask(qa, "How long is the warranty?")
    ask(qa, "What is the airspeed velocity of an unladen swallow?")
