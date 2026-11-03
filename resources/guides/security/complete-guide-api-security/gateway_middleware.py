import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.middleware("http")
async def api_gateway_middleware(request: Request, call_next):
    # 1. Request size limit
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB
        return JSONResponse(status_code=413, content={"detail": "Request too large"})
    
    # 2. API key validation (skip public endpoints)
    if request.url.path.startswith("/api/"):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return JSONResponse(status_code=401, content={"detail": "Missing API key"})
        
        key_info = validate_api_key(api_key)
        if not key_info:
            return JSONResponse(status_code=401, content={"detail": "Invalid API key"})
        
        # 3. Rate limiting
        rate_check = check_rate_limit(api_key, key_info["tier"])
        if not rate_check["allowed"]:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"},
                headers={
                    "Retry-After": str(rate_check["window"]),
                    "X-RateLimit-Limit": str(rate_check["limit"])
                }
            )
    
    # 4. Request ID for tracing
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    
    # 5. Process request
    response = await call_next(request)
    
    # 6. Add security headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    
    # 7. Remove sensitive headers from response
    response.headers.pop("Server", None)
    response.headers.pop("X-Powered-By", None)
    
    return response

def validate_api_key(api_key: str) -> dict | None:
    # Look up API key in database — compare hashes, never plaintext
    key_record = db.query(APIKey).filter(
        APIKey.key_hash == hash_api_key(api_key),
        APIKey.is_active == True
    ).first()
    if key_record:
        return {"tier": key_record.tier, "user_id": key_record.user_id}
    return None
