"""AWS Secrets Manager: create, retrieve, and rotate secrets.

Usage:
    python aws_secrets_manager.py

Prerequisites:
    pip install boto3
    AWS credentials configured with secretsmanager:* permissions.
"""

import boto3
import json


def create_secret(name: str, secret_value: dict) -> str:
    """Create a new secret in AWS Secrets Manager."""
    client = boto3.client("secretsmanager")
    response = client.create_secret(
        Name=name,
        SecretString=json.dumps(secret_value),
    )
    return response["ARN"]


def get_secret(secret_id: str) -> dict:
    """Retrieve a secret value from AWS Secrets Manager."""
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id)
    return json.loads(response["SecretString"])


def rotate_secret(secret_id: str, lambda_arn: str, days: int = 30) -> None:
    """Configure automatic rotation for a secret."""
    client = boto3.client("secretsmanager")
    client.rotate_secret(
        SecretId=secret_id,
        RotationLambdaARN=lambda_arn,
        RotationRules={"AutomaticallyAfterDays": days},
    )
    print(f"Rotation configured for {secret_id} every {days} days")


if __name__ == "__main__":
    # Create a secret
    arn = create_secret("prod/database/password", {"username": "admin", "password": "supersecret"})
    print(f"Created secret: {arn}")

    # Retrieve it
    secret = get_secret("prod/database/password")
    print(f"Retrieved: {secret}")

    # Configure rotation (uncomment with real Lambda ARN)
    # rotate_secret("prod/database/password", "arn:aws:lambda:us-east-1:123:function:rotation", 30)
