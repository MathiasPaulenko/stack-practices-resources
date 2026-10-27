# Use a minimal ASGI adapter instead of a full framework
# Instead of Flask/FastAPI (heavy init), use a raw handler
def lambda_handler(event, context):
    method = event['httpMethod']
    path = event['path']

    if method == 'GET' and path == '/health':
        return {"statusCode": 200, "body": '{"status":"ok"}'}

    if method == 'GET' and path.startswith('/products/'):
        product_id = path.split('/')[-1]
        return handle_get_product(product_id)

    return {"statusCode": 404, "body": '{"error":"not found"}'}
