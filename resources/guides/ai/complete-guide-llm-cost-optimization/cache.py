"""Exact + semantic LLM caches. Exact: dict/Redis hash. Semantic: embeddings."""
import hashlib
import json
from datetime import datetime, timedelta

import numpy as np
from openai import OpenAI

client = OpenAI()


class LLMCache:
    def __init__(self, ttl_hours: int = 24):
        self.cache: dict[str, dict] = {}
        self.ttl = timedelta(hours=ttl_hours)

    def _key(self, model: str, messages: list) -> str:
        data = json.dumps({"model": model, "messages": messages}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def get(self, model: str, messages: list):
        key = self._key(model, messages)
        if key in self.cache:
            e = self.cache[key]
            if datetime.now() - e["timestamp"] < self.ttl:
                return e["response"]
            del self.cache[key]
        return None

    def set(self, model: str, messages: list, response: str):
        self.cache[self._key(model, messages)] = {"response": response, "timestamp": datetime.now()}


class SemanticCache:
    """In-memory semantic cache — fine for ~1k entries; use a vector index beyond."""
    def __init__(self, threshold: float = 0.95, max_entries: int = 1000):
        self.entries, self.threshold, self.max_entries = [], threshold, max_entries

    def _embed(self, text: str):
        r = client.embeddings.create(model="text-embedding-3-small", input=text)
        return np.array(r.data[0].embedding)

    def get(self, query: str):
        q = self._embed(query)
        for e in self.entries:
            if np.dot(q, e["embedding"]) / (np.linalg.norm(q) * np.linalg.norm(e["embedding"])) >= self.threshold:
                return e["response"]
        return None

    def set(self, query: str, response: str):
        self.entries.append({"query": query, "response": response, "embedding": self._embed(query)})
        if len(self.entries) > self.max_entries:
            self.entries.pop(0)
