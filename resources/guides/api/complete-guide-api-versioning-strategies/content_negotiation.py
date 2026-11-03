from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: str, request: Request):
    accept = request.headers.get("accept", "")

    if "application/vnd.example.v1+json" in accept:
        return {"id": user_id, "name": "Alice"}
    elif "application/vnd.example.v2+json" in accept:
        return {"id": user_id, "name": "Alice", "email": "alice@example.com"}

    raise HTTPException(status_code=406, detail="Unsupported media type")
