import boto3

# Cheap clients can live at module level; heavy resources go lazy
_dynamodb = None
_s3 = None

def get_dynamodb():
    global _dynamodb
    if _dynamodb is None:
        _dynamodb = boto3.resource("dynamodb")
    return _dynamodb

def get_s3():
    global _s3
    if _s3 is None:
        _s3 = boto3.client("s3")
    return _s3

def handler(event, context):
    # Only initialize what this invocation actually needs
    if event["path"] == "/users":
        return get_dynamodb().Table("users").scan()
    if event["path"].startswith("/files/"):
        return get_s3().get_object(Bucket="assets", Key=event["path"])
