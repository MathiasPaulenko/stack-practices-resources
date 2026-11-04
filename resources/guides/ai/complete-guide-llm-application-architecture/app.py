"""FastAPI app wiring every layer from the guide: SSE streaming + typed request.

Run:  uvicorn app:app --reload
Test: curl -N -X POST localhost:8000/chat -H 'content-type: application/json' -d '{"message":"hi"}'
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from pydantic import BaseModel
import json

app = FastAPI()
client = AsyncOpenAI()


class ChatRequest(BaseModel):
    message: str
    system: str = "You are a helpful assistant."


@app.post("/chat")
async def chat(request: ChatRequest):
    async def stream_response():
        stream = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": request.system},
                {"role": "user", "content": request.message},
            ],
            stream=True,
            temperature=0.7,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'type': 'token', 'content': chunk.choices[0].delta.content})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")
