import chromadb
from openai import OpenAI

client = OpenAI()

class LongTermMemory:
    def __init__(self, collection_name: str = "agent_memory"):
        self.db = chromadb.PersistentClient(path="./agent_memory")
        self.collection = self.db.get_or_create_collection(collection_name)
    
    def store(self, content: str, metadata: dict = None):
        embedding = client.embeddings.create(
            model="text-embedding-3-small",
            input=content
        ).data[0].embedding
        
        import hashlib
        doc_id = hashlib.md5(content.encode()).hexdigest()
        
        self.collection.add(
            ids=[doc_id],
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata or {}]
        )
    
    def recall(self, query: str, n_results: int = 5) -> list[str]:
        query_embedding = client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        ).data[0].embedding
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results["documents"][0]
    
    def get_context(self, query: str) -> str:
        memories = self.recall(query)
        if memories:
            return "Previous relevant context:\n" + "\n".join(f"- {m}" for m in memories)
        return ""

# Usage in agent
memory = LongTermMemory()

# Store important facts
memory.store("User prefers Python over JavaScript", {"type": "preference"})
memory.store("User's project uses FastAPI and PostgreSQL", {"type": "project_info"})

# Recall during agent execution
context = memory.get_context("What language should I use?")
# Returns stored preferences
