"""AWS Secrets Manager rotation Lambda (single-user strategy).

Secrets Manager invokes this handler once per step:
  createSecret -> setSecret -> testSecret -> finishSecret

Every step must be idempotent — Secrets Manager retries steps on failure.
The rotation event only carries SecretId, ClientRequestToken and Step;
it does NOT include a CurrentVersionId field.

Deploy notes:
- psycopg2 is not in the Lambda runtime. Package psycopg2-binary as a
  Lambda layer or include it in the deployment bundle.
- Prefer the managed "alternating users" strategy for RDS when possible;
  use this template for engines without managed rotation.
"""
import json
import secrets

import boto3
import psycopg2
from psycopg2 import sql


def lambda_handler(event, context):
    secret_arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    client = boto3.client('secretsmanager')

    if step == 'createSecret':
        # Generate a new secret version staged as AWSPENDING
        current = json.loads(client.get_secret_value(SecretId=secret_arn)['SecretString'])
        new_password = secrets.token_urlsafe(32)
        new_secret = {**current, 'password': new_password}
        client.put_secret_value(
            SecretId=secret_arn,
            ClientRequestToken=token,
            SecretString=json.dumps(new_secret),
        )

    elif step == 'setSecret':
        # Apply the pending password in the database
        pending = client.get_secret_value(
            SecretId=secret_arn,
            VersionStage='AWSPENDING',
            VersionId=token,
        )
        pending_creds = json.loads(pending['SecretString'])
        current = json.loads(client.get_secret_value(SecretId=secret_arn)['SecretString'])

        conn = psycopg2.connect(
            host=current['host'],
            user=current['username'],
            password=current['password'],
        )
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("ALTER USER {} WITH PASSWORD %s").format(
                    sql.Identifier(pending_creds['username'])
                ),
                (pending_creds['password'],),
            )
        conn.commit()
        conn.close()

    elif step == 'testSecret':
        # Verify the pending credentials connect
        pending = client.get_secret_value(
            SecretId=secret_arn,
            VersionStage='AWSPENDING',
            VersionId=token,
        )
        creds = json.loads(pending['SecretString'])
        conn = psycopg2.connect(
            host=creds['host'],
            user=creds['username'],
            password=creds['password'],
        )
        conn.close()

    elif step == 'finishSecret':
        # Promote AWSPENDING to AWSCURRENT. The event does not carry the
        # current version id — look it up via describe_secret.
        versions = client.describe_secret(SecretId=secret_arn)['VersionIdsToStages']
        current_version_id = next(
            vid for vid, stages in versions.items() if 'AWSCURRENT' in stages
        )
        client.update_secret_version_stage(
            SecretId=secret_arn,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token,
            RemoveFromVersionId=current_version_id,
        )

    else:
        raise ValueError(f"Unknown rotation step: {step}")
