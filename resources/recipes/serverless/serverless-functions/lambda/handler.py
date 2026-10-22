"""AWS Lambda handler from the recipe — invocable locally with a fake event.

Run locally (no AWS needed):
    python handler.py

Deploy:
    zip the file as your function package; the Lambda entrypoint is
    `handler` (file name + function name).
"""

import json


def handler(event, context):
    # Extract query parameter
    name = event.get("queryStringParameters", {}).get("name", "World")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": f"Hello, {name}!"}),
    }


if __name__ == "__main__":
    # Same shape Lambda delivers for an API Gateway proxy request.
    event = {"queryStringParameters": {"name": "Mathias"}}
    result = handler(event, context=None)
    print(json.dumps(json.loads(result["body"]), indent=2))
    assert result["statusCode"] == 200
