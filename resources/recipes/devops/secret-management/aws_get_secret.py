import boto3
import json

client = boto3.client('secretsmanager')


def get_secret(secret_name):
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])


if __name__ == '__main__':
    db_creds = get_secret('prod/db/postgres')
    print(f"host={db_creds['host']} user={db_creds['username']}")
