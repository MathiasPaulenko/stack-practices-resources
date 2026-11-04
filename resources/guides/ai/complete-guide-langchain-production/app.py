"""FastAPI endpoint streaming an LCEL chain over SSE.

Run:  uvicorn app:app --reload
Test: curl -N -X POST localhost:8000/chat -H 'content-type: application/json' -d '{"question":"hi"}'
"""
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel

app = FastAPI()

model = ChatOpenAI(model="gpt-4o", streaming=True)
prompt = ChatPromptTemplate.from_template("Answer: {question}")
chain = prompt | model | StrOutputParser()


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
async def chat(request: ChatRequest):
    async def stream():
        async for chunk in chain.astream({"question": request.question}):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.post("/chat/sync")
async def chat_sync(request: ChatRequest):
    result = await chain.ainvoke({"question": request.question})
    return {"answer": result}
