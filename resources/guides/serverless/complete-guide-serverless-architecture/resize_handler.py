"""S3-triggered Lambda: resizes uploaded images and notifies via SQS.

Pipeline step 2 of the guide's worked example:
  S3 upload -> resize Lambda -> resized S3 keys -> SQS message

Environment variables:
    OUTPUT_BUCKET: destination bucket for resized images
    QUEUE_URL:     SQS queue URL for the metadata step
"""

import io
import json
import os
import uuid

import boto3
from PIL import Image

# Initialized once per container lifecycle (reused across invocations)
s3 = boto3.client("s3")
sqs = boto3.client("sqs")

SIZES = {
    "thumbnail": (100, 100),
    "medium": (500, 500),
    "large": (1200, 1200),
}


def lambda_handler(event, context):
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    image = Image.open(io.BytesIO(read_object(bucket, key)))

    keys = {}
    for version, size in SIZES.items():
        out_key = f"uploads/resized/{uuid.uuid4()}-{version}.jpg"
        resized = image.copy()
        resized.thumbnail(size)
        buf = io.BytesIO()
        resized.convert("RGB").save(buf, format="JPEG")
        buf.seek(0)
        s3.put_object(Bucket=os.environ["OUTPUT_BUCKET"], Key=out_key, Body=buf)
        keys[f"{version}Key"] = out_key

    sqs.send_message(
        QueueUrl=os.environ["QUEUE_URL"],
        MessageBody=json.dumps({"originalKey": key, "imageId": str(uuid.uuid4()), **keys}),
    )
    return {"statusCode": 200, "body": json.dumps({"processed": key})}


def read_object(bucket, key):
    return s3.get_object(Bucket=bucket, Key=key)["Body"].read()
