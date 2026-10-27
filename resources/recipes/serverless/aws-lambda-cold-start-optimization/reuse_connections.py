import json
import boto3
import os

# Module-level: runs once per execution environment
# These persist across warm invocations
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

# But keep it light — only clients, not data
def lambda_handler(event, context):
    # Warm invocation reuses the table client
    response = table.get_item(Key={'id': event['pathParameters']['id']})
    return {
        "statusCode": 200,
        "body": json.dumps(response.get('Item', {})),
    }
