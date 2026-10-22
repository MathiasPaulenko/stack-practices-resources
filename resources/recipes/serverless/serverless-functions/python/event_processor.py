"""S3-triggered event processing logic — locally verifiable without AWS.

The recipe's handler calls s3.get_object and sns.publish. Here the cloud
clients are replaced by injected fakes so the record-processing loop is
testable with plain Python:

    python event_processor.py
"""

import json


def process_records(event, s3_client, sns_client, topic_arn):
    """Process each S3 record and publish a summary to SNS.

    Returns the count of processed records. Safe to re-run: publishing the
    same summary twice is harmless (idempotent by design).
    """
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read().decode("utf-8")

        sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(
                {
                    "file": key,
                    "size": len(content),
                    "lines": content.count("\n"),
                }
            ),
        )

    return len(event["Records"])


class _FakeBody:
    def read(self):
        return b"alpha\nbeta\ngamma\n"


class FakeS3:
    def get_object(self, Bucket, Key):
        return {"Body": _FakeBody()}


class FakeSNS:
    def __init__(self):
        self.messages = []

    def publish(self, TopicArn, Message):
        self.messages.append(json.loads(Message))


if __name__ == "__main__":
    event = {
        "Records": [
            {"s3": {"bucket": {"name": "uploads"}, "object": {"key": "data.csv"}}},
            {"s3": {"bucket": {"name": "uploads"}, "object": {"key": "other.csv"}}},
        ]
    }
    sns = FakeSNS()
    n = process_records(event, FakeS3(), sns, "arn:aws:sns:us-east-1:1:done")
    print(f"processed={n}")
    print(f"published={json.dumps(sns.messages)}")
    assert n == 2 and sns.messages[0]["lines"] == 3
