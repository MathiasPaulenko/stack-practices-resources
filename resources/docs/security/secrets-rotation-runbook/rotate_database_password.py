"""Rotate a database password stored in AWS Secrets Manager.

Reads the current credentials, generates a new password, updates the
database user, writes the new version back to Secrets Manager, and
verifies connectivity before reporting success.

Usage:
    python rotate_database_password.py <secret_id>

Requires: boto3, psycopg2-binary
"""
import sys
import json
import secrets
from datetime import datetime, timezone

import boto3
import psycopg2
from psycopg2 import sql


def rotate_database_password(secret_id: str) -> None:
    client = boto3.client('secretsmanager')

    # Step 1: get the current secret
    current = client.get_secret_value(SecretId=secret_id)
    current_creds = json.loads(current['SecretString'])

    # Step 2: generate the new password
    new_password = secrets.token_urlsafe(32)

    # Step 3: connect to the database with the current credentials
    conn = psycopg2.connect(
        host=current_creds['host'],
        user=current_creds['username'],
        password=current_creds['password'],
        database=current_creds['dbname'],
    )

    # Step 4: update the password in the database (ALTER USER)
    # Identifiers can't be parameterized — use sql.Identifier, not f-strings
    with conn.cursor() as cur:
        cur.execute(
            sql.SQL("ALTER USER {} WITH PASSWORD %s").format(
                sql.Identifier(current_creds['username'])
            ),
            (new_password,),
        )
    conn.commit()
    conn.close()

    # Step 5: write the new secret version to Secrets Manager
    new_creds = current_creds.copy()
    new_creds['password'] = new_password
    client.put_secret_value(
        SecretId=secret_id,
        SecretString=json.dumps(new_creds),
    )

    # Step 6: verify the new credentials actually connect
    conn = psycopg2.connect(
        host=new_creds['host'],
        user=new_creds['username'],
        password=new_password,
        database=new_creds['dbname'],
    )
    conn.close()

    print(f"Rotation complete for {secret_id} at {datetime.now(timezone.utc)}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    rotate_database_password(sys.argv[1])
