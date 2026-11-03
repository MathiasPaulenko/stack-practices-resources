from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def router(path: str, request: Request):
    # New endpoints handled by v2
    if path.startswith("v2/"):
        return await handle_v2(request)

    # Old endpoints — check if migrated
    migrated = ["users", "orders"]  # endpoints that moved to v2
    base_path = path.split("/", 1)[0] if "/" in path else path

    if base_path in migrated:
        # Proxy to v2 with response transformation
        return await proxy_to_v2(request)

    # Not migrated — serve from v1
    return await handle_v1(request)
