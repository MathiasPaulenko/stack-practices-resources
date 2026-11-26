import os
from functools import lru_cache


@lru_cache(maxsize=1)
def get_secrets():
    """Load secrets once at startup, cache for process lifetime."""
    if os.environ.get('ENVIRONMENT') == 'production':
        import boto3
        import json
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId='prod/app/secrets')
        return json.loads(response['SecretString'])
    else:
        from dotenv import load_dotenv
        load_dotenv()
        return dict(os.environ)


if __name__ == '__main__':
    app_secrets = get_secrets()
    print('DATABASE_URL set:', 'DATABASE_URL' in app_secrets)
