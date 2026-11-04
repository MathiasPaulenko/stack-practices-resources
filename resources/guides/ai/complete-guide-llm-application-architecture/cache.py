"""Exact + semantic LLM caches on Redis.

NOTE: the semantic lookup scans cached embeddings — fine for hundreds of
entries. At scale, move vectors to Redis Stack (FT.SEARCH KNN) or pgvector.
"""
import hashlib
import json

import numpy as np
import redis
from openai import AsyncOpenAI

r = redis.Redis(host="localhost", port=6379)
client = AsyncOpenAI()


def exact_cache_key(messages: list[dict], model: str) -> str:
    content = json.dumps({"messages": messages, "model": model})
    return f"llm_exact:{hashlib.sha256(content.encode()).hexdigest()}"


async def exact_cached_completion(messages, model="gpt-4o"):
    key = exact_cache_key(messages, model)
    if cached := r.get(key):
        return json.loads(cached)
    response = await client.chat.completions.create(model=model, messages=messages)
    result = response.choices[0].message.content
    r.setex(key, 3600, json.dumps(result))
    return result


async def get_embedding(text: str) -> list[float]:
    response = await client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def cosine_similarity(a, b) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


async def semantic_cached_completion(messages: list[dict], threshold: float = 0.95) -> str:
    user_query = messages[-1]["content"]
    query_embedding = await get_embedding(user_query)

    for key in r.scan_iter("llm_cache:*", count=100):
        cached = json.loads(r.get(key))
        if cosine_similarity(query_embedding, cached["embedding"]) > threshold:
            return cached["response"]

    response = await client.chat.completions.create(model="gpt-4o", messages=messages)
    result = response.choices[0].message.content
    r.setex(
        f"llm_cache:{hashlib.md5(user_query.encode()).hexdigest()}",
        3600,
        json.dumps({"query": user_query, "embedding": query_embedding, "response": result}),
    )
    return result
