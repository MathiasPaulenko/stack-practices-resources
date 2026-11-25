"""Request ID middleware: every response carries X-Request-ID.

When a consumer reports "it failed", the ID in their response
points straight at their request in your logs.
"""

import uuid

from fastapi import FastAPI

app = FastAPI()


@app.middleware("http")
async def request_id_middleware(request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
