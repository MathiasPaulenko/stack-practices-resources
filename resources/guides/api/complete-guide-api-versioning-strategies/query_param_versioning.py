from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: str, request: Request):
    version = request.query_params.get("version", "1")

    if version == "1":
        return {"id": user_id, "name": "Alice"}
    elif version == "2":
        return {"id": user_id, "name": "Alice", "email": "alice@example.com"}
    raise HTTPException(status_code=400, detail="Unsupported version")
