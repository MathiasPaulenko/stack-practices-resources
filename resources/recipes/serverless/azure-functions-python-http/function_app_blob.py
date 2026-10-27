import azure.functions as func
import logging

app = func.FunctionApp()

@app.blob_trigger(
    arg_name="blob",
    path="uploads/{name}",
    connection="StorageConnection",
)
def process_upload(blob: func.InputStream) -> None:
    logging.info(f"Processing blob: {blob.name}, size: {blob.length} bytes")
    content = blob.read()
    process_file(content)
