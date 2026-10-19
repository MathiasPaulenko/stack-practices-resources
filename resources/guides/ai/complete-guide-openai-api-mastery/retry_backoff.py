"""Rate limiting (token bucket) plus error-type-aware retry with backoff."""
import asyncio
import random
import time

from openai import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AsyncOpenAI,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
)

client = AsyncOpenAI()


class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.interval = 60.0 / requests_per_minute
        self.last_request = 0.0

    async def wait(self):
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.interval:
            await asyncio.sleep(self.interval - elapsed)
        self.last_request = time.time()


limiter = RateLimiter(requests_per_minute=50)


async def robust_call(messages, max_retries=5):
    """Retry transient failures; never retry auth or bad requests."""
    for attempt in range(max_retries):
        try:
            await limiter.wait()
            return await client.chat.completions.create(
                model="gpt-4o", messages=messages
            )
        except AuthenticationError:
            raise RuntimeError("Invalid API key. Check OPENAI_API_KEY.")
        except BadRequestError as e:
            raise RuntimeError(f"Bad request: {e}")
        except RateLimitError as e:
            delay = getattr(e, "retry_after", 2**attempt) + random.uniform(0, 1)
            print(f"Rate limited. Retrying in {delay:.1f}s...")
            await asyncio.sleep(delay)
        except (APITimeoutError, APIConnectionError):
            await asyncio.sleep(2**attempt + random.uniform(0, 1))
        except APIError as e:
            raise RuntimeError(f"OpenAI API error: {e}")

    raise RuntimeError("Max retries exceeded")


if __name__ == "__main__":
    result = asyncio.run(
        robust_call([{"role": "user", "content": "Say hi in one word."}])
    )
    print(result.choices[0].message.content)
