"""RDS connection through RDS Proxy with guaranteed cleanup.

Source: https://stackpractices.com/guides/complete-guide-aws-lambda-production/
"""
import os
import json
import psycopg2


def get_db_connection(secret: dict) -> psycopg2.extensions.connection:
    # Point at the PROXY endpoint, not the RDS instance directly
    return psycopg2.connect(
        host=os.environ["DB_PROXY_ENDPOINT"],
        dbname=os.environ["DB_NAME"],
        user=secret["username"],
        password=secret["password"],
    )


def lambda_handler(event, context, secret=None):
    conn = get_db_connection(secret or {"username": "u", "password": "p"})
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s",
                       (event["user_id"],))
        user = cursor.fetchone()
        return {"statusCode": 200,
                "body": json.dumps(user, default=str)}
    finally:
        cursor.close()
        conn.close()
