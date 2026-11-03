from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/api/v1/users/{user_id}")
async def get_user_v1(user_id: str, response: Response):
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = "Sun, 01 Jun 2025 00:00:00 GMT"
    response.headers["Link"] = '</api/v2/users/{user_id}>; rel="successor-version"'
    return {"id": user_id, "name": "Alice"}
