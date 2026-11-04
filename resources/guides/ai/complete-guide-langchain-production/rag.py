"""RAG pipeline: load -> split -> embed -> retrieve -> answer with sources.

Needs a text file to index:
    echo "Vacation policy: 20 days per year." > docs/handbook.txt
    OPENAI_API_KEY=... python rag.py
"""
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

loader = TextLoader("docs/handbook.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", ". ", " "]
)
chunks = splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})


def format_docs(docs):
    return "\n\n".join(f"[Source {i+1}]: {doc.page_content}" for i, doc in enumerate(docs))


rag_prompt = ChatPromptTemplate.from_template("""
Answer the question based on the context below. Cite source numbers.

Context:
{context}

Question: {question}
""")

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | ChatOpenAI(model="gpt-4o", temperature=0.3)
    | StrOutputParser()
)

if __name__ == "__main__":
    print(rag_chain.invoke("What is the vacation policy?"))
