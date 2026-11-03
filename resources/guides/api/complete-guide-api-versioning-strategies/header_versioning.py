from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(
    user_id: str,
    x_api_version: str = Header(default="1", alias="X-API-Version"),
):
    if x_api_version == "1":
        return {"id": user_id, "name": "Alice"}
    elif x_api_version == "2":
        return {"id": user_id, "name": "Alice", "email": "alice@example.com"}
    raise HTTPException(status_code=400, detail="Unsupported version")
