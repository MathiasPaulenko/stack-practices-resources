"""Consistent error envelope for a REST API.

Every non-2xx response shares the same shape:
{code, message, field?, documentation_url, trace_id}
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, field: str | None = None):
        self.status = status
        self.code = code
        self.message = message
        self.field = field


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError) -> JSONResponse:
    body = {
        "error": {
            "code": exc.code,
            "message": exc.message,
            "documentation_url": f"https://docs.example.com/errors/{exc.code}",
            "trace_id": request.headers.get("x-request-id", "unknown"),
        }
    }
    if exc.field:
        body["error"]["field"] = exc.field
    return JSONResponse(status_code=exc.status, content=body)


@app.post("/v1/users")
async def create_user(payload: dict):
    if "email" not in payload:
        raise ApiError(422, "MISSING_FIELD", "Field 'email' is required.", field="email")
    if "@" not in payload["email"]:
        raise ApiError(422, "INVALID_EMAIL", "The email format is invalid.", field="email")
    return {"id": "usr_001", **payload}
