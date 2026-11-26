import os
import jwt

JWT_SECRET = os.environ['JWT_SECRET']
PERMISSIONS = {
    'admin': ['GET', 'POST', 'PUT', 'DELETE'],
    'editor': ['GET', 'POST', 'PUT'],
    'user': ['GET'],
}


def lambda_handler(event, context):
    try:
        token = extract_token(event)
        claims = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        role = claims.get('role', 'user')
        allowed = PERMISSIONS.get(role, [])
        effect = 'Allow' if event['httpMethod'] in allowed else 'Deny'
        return generate_policy(claims['sub'], effect, event['routeArn'], {
            'userId': claims['sub'],
            'role': role,
        })
    except Exception as e:
        print(f"Auth error: {e}")
        return generate_policy('error', 'Deny', event['routeArn'], {})


def extract_token(event):
    headers = event.get('headers', {})
    auth_header = headers.get('Authorization') or headers.get('authorization', '')
    if not auth_header.startswith('Bearer '):
        raise ValueError("Missing Authorization header")
    return auth_header[7:]


def generate_policy(principal_id, effect, resource, context):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource,
            }],
        },
        'context': context,
    }
