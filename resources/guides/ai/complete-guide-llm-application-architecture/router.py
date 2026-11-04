"""Model router + retry/fallback across providers."""
import asyncio

from openai import AsyncOpenAI, APIError, RateLimitError

client = AsyncOpenAI()


class ModelRouter:
    def __init__(self):
        self.routes = {
            "simple_qa": "gpt-4o-mini",
            "complex_reasoning": "gpt-4o",
            "code_gener
