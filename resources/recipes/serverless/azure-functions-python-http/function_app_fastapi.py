import azure.functions as func
from fastapi import FastAPI

fastapi_app = FastAPI()

@fastapi_app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="{*route}", methods=["GET", "POST", "PUT", "DELETE"])
async def asgi_handler(req: func.HttpRequest) -> func.HttpResponse:
    return await func.AsgiMiddleware(fastapi_app).handle_async(req)
