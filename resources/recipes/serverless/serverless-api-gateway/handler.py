import json

def lambda_handler(event, context):
    # API Gateway passes HTTP data in the event object
    method = event['httpMethod']
    path = event['path']
    query = event.get('queryStringParameters', {})

    if method == 'GET' and path == '/users':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'users': ['alice', 'bob']})
        }

    if method == 'POST' and path == '/users':
        body = json.loads(event['body'])
        return {
            'statusCode': 201,
            'body': json.dumps({'id': '123', 'name': body['name']})
        }

    return {'statusCode': 404, 'body': json.dumps({'error': 'Not found'})}
