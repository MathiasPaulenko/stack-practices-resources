"""Token streaming plus a FastAPI SSE endpoint that proxies the model."""
import asyncio
import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI, OpenAI

app = FastAPI()
async_client = AsyncOpenAI()


def sync_stream() -> None:
    client = OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Write a poem about Python."}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)


@app.post("/chat/stream")
async def chat_stream(request: dict):
    async def generate():
        stream = await async_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request["message"]},
            ],
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                data = json.dumps({"token": chunk.choices[0].delta.content})
                yield f"data: {data}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


if __name__ == "__main__":
    sync_stream()
    # uvicorn streaming_sse:app --reload
