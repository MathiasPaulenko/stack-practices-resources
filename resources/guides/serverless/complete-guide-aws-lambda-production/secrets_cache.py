"""Secrets Manager fetch cached once per execution environment via lru_cache.

Source: https://stackpractices.com/guides/complete-guide-aws-lambda-production/
"""
import json
import os
from functools import lru_cache

import boto3


@lru_cache(maxsize=1)
def get_db_credentials() -> dict:
    """Loaded once per environment; warm invocations reuse the cache."""
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(
        SecretId=os.environ["DB_SECRET_ARN"])
    return json.loads(response["SecretString"])
