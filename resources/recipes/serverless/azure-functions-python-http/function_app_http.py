# function_app.py
import azure.functions as func
import json
import logging

app = func.FunctionApp()

@app.route(route="users/{user_id}", methods=["GET"])
def get_user(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.route_params.get('user_id')

    user = fetch_user_from_db(user_id)
    if not user:
        return func.HttpResponse(
            body=json.dumps({"error": "User not found"}),
            status_code=404,
            mimetype="application/json",
        )

    return func.HttpResponse(
        body=json.dumps(user),
        status_code=200,
        mimetype="application/json",
    )

@app.route(route="users", methods=["POST"])
def create_user(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            body=json.dumps({"error": "Invalid JSON"}),
            status_code=400,
            mimetype="application/json",
        )

    user = create_user_in_db(body)
    return func.HttpResponse(
        body=json.dumps(user),
        status_code=201,
        mimetype="application/json",
    )
