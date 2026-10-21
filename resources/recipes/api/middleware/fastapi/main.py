"""FastAPI middleware chain from the StackPractices middleware recipe.

Run: uvicorn main:app --port 8000
Then: curl http://localhost:8000/api/protected -H "Authorization: Bearer x"
"""

import time

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(
        f"{request.method} {request.url.path} "
        f"- {response.status_code} ({duration:.3f}s)"
    )
    return response


# CORS — added before auth middleware so preflights survive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_methods=["GET", "POST"],
)


async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    return token


@app.get("/api/protected", dependencies=[Depends(verify_token)])
async def protected():
    return {"message": "Secret data"}


@app.get("/boom")
async def boom():
    raise RuntimeError("intentional failure")
