# lambda_function.py
import json
import requests  # From the layer
from pydantic import BaseModel  # From the layer

class ApiResponse(BaseModel):
    status: str
    data: dict

def lambda_handler(event, context):
    response = requests.get("https://api.example.com/data")
    api_data = ApiResponse(status="ok", data=response.json())
    return {
        "statusCode": 200,
        "body": json.dumps(api_data.model_dump()),
    }
