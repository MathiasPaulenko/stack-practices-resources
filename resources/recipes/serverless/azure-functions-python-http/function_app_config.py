import os
import azure.functions as func

app = func.FunctionApp()

@app.route(route="config")
def get_config(req: func.HttpRequest) -> func.HttpResponse:
    api_key = os.environ.get("API_KEY", "not-set")
    cosmos_conn = os.environ.get("CosmosDBConnection", "not-set")

    return func.HttpResponse(
        body=json.dumps({
            "api_key_configured": api_key != "not-set",
            "cosmos_configured": cosmos_conn != "not-set",
        }),
        status_code=200,
        mimetype="application/json",
    )
