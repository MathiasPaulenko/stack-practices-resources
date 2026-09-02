"""FastAPI application with RFC 7807 Problem Details error handling."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Handle Errors Demo")


class ProblemDetail(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str
    instance: str | None = None


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "type": "https://api.example.com/errors/invalid-input",
            "title": "Invalid Input",
            "detail": str(exc),
            "status": 400,
            "instance": str(request.url),
        },
        media_type="application/problem+json",
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, dict) else {"detail": exc.detail}
    content = {
        "type": detail.get("type", "about:blank"),
        "title": detail.get("title", "HTTP Error"),
        "detail": detail.get("detail", str(exc.detail)),
        "status": exc.status_code,
        "instance": str(request.url),
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        media_type="application/problem+json",
    )


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(
            status_code=404,
            detail={
                "type": "https://api.example.com/errors/not-found",
                "title": "User Not Found",
                "detail": f"No user with id {user_id}",
                "status": 404,
            },
        )
    return {"id": user_id, "name": "Ada"}


@app.get("/crash")
async def crash():
    raise RuntimeError("Intentional crash for testing")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
