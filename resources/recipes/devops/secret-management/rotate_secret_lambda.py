import boto3
import json
import secrets
import string

import psycopg2


def rotate_secret(event, context):
    client = boto3.client('secretsmanager')
    secret_arn = event['SecretId']
    token = event['ClientRequestToken']

    current = client.get_secret_value(SecretId=secret_arn, VersionStage='AWSCURRENT')
    creds = json.loads(current['SecretString'])

    new_password = generate_secure_password()

    conn = psycopg2.connect(
        host=creds['host'],
        user=creds['username'],
        password=creds['password'],
        dbname='postgres'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"ALTER USER {creds['username']} WITH PASSWORD '{new_password}'")
    cursor.close()
    conn.close()

    new_secret = json.dumps({**creds, 'password': new_password})
    client.put_secret_value(
        SecretId=secret_arn,
        SecretString=new_secret,
        VersionStage='AWSPENDING'
    )
    client.update_secret_version_stage(
        SecretId=secret_arn,
        VersionStage='AWSCURRENT',
        MoveToVersion=token,
        RemoveFromVersion=current['VersionId']
    )


def generate_secure_password(length=32):
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(alphabet) for _ in range(length))
