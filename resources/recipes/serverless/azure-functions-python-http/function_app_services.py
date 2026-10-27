import azure.functions as func
import json
from dataclasses import dataclass

app = func.FunctionApp()

@dataclass
class UserService:
    db_connection_string: str

    def get_user(self, user_id: str) -> dict:
        # In production, use a real database client
        return {"id": user_id, "name": "Alice", "email": "alice@example.com"}

# Module-level: one instance per warm worker, reused across invocations
_user_service = UserService(db_connection_string="")

@app.route(route="users/{user_id}")
def get_user(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get('user_id')
    user = _user_service.get_user(user_id)

    if not user:
        return func.HttpResponse(
            body=json.dumps({"error": "Not found"}),
            status_code=404,
            mimetype="application/json",
        )
    return func.HttpResponse(
        body=json.dumps(user),
        status_code=200,
        mimetype="application/json",
    )
