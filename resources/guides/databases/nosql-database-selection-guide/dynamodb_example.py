"""DynamoDB access patterns from the NoSQL selection guide.

Companion to https://stackpractices.com/guides/nosql-database-selection-guide/
Requires: boto3, a DynamoDB table named 'Users' (partition key user_id,
sort key timestamp). Works against DynamoDB Local too:

    aws dynamodb create-table \
        --table-name Users \
        --attribute-definitions AttributeName=user_id,AttributeType=S AttributeName=timestamp,AttributeType=S \
        --key-schema AttributeName=user_id,KeyType=HASH AttributeName=timestamp,KeyType=RANGE \
        --billing-mode PAY_PER_REQUEST \
        --endpoint-url http://localhost:8000
"""

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Users")

# Get by partition key (single-digit ms latency)
table.get_item(Key={"user_id": "user-123"})

# Query by partition + sort key
table.query(
    KeyConditionExpression=Key("user_id").eq("user-123")
    & Key("timestamp").gt("2024-01-01")
)
