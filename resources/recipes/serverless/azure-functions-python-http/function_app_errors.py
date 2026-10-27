import azure.functions as func
import json
import logging
import traceback
import functools

app = func.FunctionApp()

def handle_errors(fn):
    @functools.wraps(fn)
    async def wrapper(req: func.HttpRequest) -> func.HttpResponse:
        try:
            return await fn(req)
        except ValueError as e:
            logging.error(f"Validation error: {e}")
            return func.HttpResponse(
                body=json.dumps({"error": str(e)}),
                status_code=400,
                mimetype="application/json",
            )
        except Exception as e:
            logging.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
            return func.HttpResponse(
                body=json.dumps({"error": "Internal server error"}),
                status_code=500,
                mimetype="application/json",
            )
    return wrapper

@app.route(route="orders", methods=["POST"])
@handle_errors
async def create_order(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()

    if not body.get("product_id"):
        raise ValueError("product_id is required")
    if not body.get("quantity") or body["quantity"] <= 0:
        raise ValueError("quantity must be positive")

    order = await process_order(body)
    return func.HttpResponse(
        body=json.dumps(order),
        status_code=201,
        mimetype="application/json",
    )
