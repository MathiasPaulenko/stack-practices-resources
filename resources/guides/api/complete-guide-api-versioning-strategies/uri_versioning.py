from fastapi import FastAPI, APIRouter

app = FastAPI()

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/users/{user_id}")
async def get_user_v1(user_id: str):
    return {"id": user_id, "name": "Alice", "email": "alice@example.com"}

@v2_router.get("/users/{user_id}")
async def get_user_v2(user_id: str):
    return {"id": user_id, "name": "Alice", "email": "alice@example.com", "created_at": "2024-01-01"}

app.include_router(v1_router)
app.include_router(v2_router)
