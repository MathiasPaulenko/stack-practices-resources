import azure.functions as func
import json

app = func.FunctionApp()

# Cosmos DB input binding — fetch document by ID
@app.route(route="documents/{doc_id}")
@app.cosmos_db_input(
    arg_name="document",
    database_name="mydb",
    container_id="documents",
    id="{doc_id}",
    partition_key="{doc_id}",
    connection="CosmosDBConnection",
)
def get_document(req: func.HttpRequest, document: func.Document) -> func.HttpResponse:
    if document is None:
        return func.HttpResponse(
            body=json.dumps({"error": "Document not found"}),
            status_code=404,
            mimetype="application/json",
        )
    return func.HttpResponse(
        body=json.dumps(document.to_dict()),
        status_code=200,
        mimetype="application/json",
    )

# Cosmos DB output binding — save document
@app.route(route="documents", methods=["POST"])
@app.cosmos_db_output(
    arg_name="output",
    database_name="mydb",
    container_id="documents",
    connection="CosmosDBConnection",
)
def create_document(req: func.HttpRequest, output: func.Out[func.Document]) -> func.HttpResponse:
    body = req.get_json()
    output.set(func.Document.from_dict(body))
    return func.HttpResponse(
        body=json.dumps({"status": "created"}),
        status_code=201,
        mimetype="application/json",
    )
