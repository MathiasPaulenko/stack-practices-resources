import time
import os
import jwt

JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGORITHM = 'HS256'


def lambda_handler(event, context):
    try:
        token = extract_token(event)
        claims = validate_jwt(token)
        return generate_policy(
            principal_id=claims['sub'],
            effect='Allow',
            resource=event['routeArn'],
            context={
                'userId': claims['sub'],
                'email': claims.get('email', ''),
                'role': claims.get('role', 'user'),
            },
        )
    except Exception as e:
        print(f"Authorization failed: {e}")
        return generate_policy('unauthorized', 'Deny', event['routeArn'], {})


def extract_token(event):
    headers = event.get('headers', {})
    auth_header = headers.get('Authorization') or headers.get('authorization', '')
    if not auth_header.startswith('Bearer '):
        raise ValueError("Missing or invalid Authorization header")
    return auth_header[7:]


def validate_jwt(token):
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if claims.get('exp', 0) < time.time():
            raise ValueError("Token expired")
        return claims
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")


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
