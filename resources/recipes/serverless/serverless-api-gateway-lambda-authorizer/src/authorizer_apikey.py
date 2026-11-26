import os
import boto3
import hashlib

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['API_KEYS_TABLE'])


def lambda_handler(event, context):
    api_key = event.get('headers', {}).get('x-api-key', '')
    if not api_key:
        return generate_deny(event['routeArn'], 'Missing API key')

    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    response = table.get_item(Key={'apiKeyHash': key_hash})

    if 'Item' not in response:
        return generate_deny(event['routeArn'], 'Invalid API key')

    item = response['Item']
    if item.get('status') != 'active':
        return generate_deny(event['routeArn'], 'API key inactive')

    return generate_allow(item['clientId'], event['routeArn'], {
        'clientId': item['clientId'],
        'tier': item.get('tier', 'free'),
    })


def generate_allow(principal_id, resource, context):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Allow',
                'Resource': resource,
            }],
        },
        'context': context,
    }


def generate_deny(resource, reason):
    return {
        'principalId': 'unauthorized',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': 'Deny',
                'Resource': resource,
            }],
        },
        'context': {'denyReason': reason},
    }
