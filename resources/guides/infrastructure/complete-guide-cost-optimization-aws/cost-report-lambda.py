"""Monthly AWS cost report by service, posted to Slack.

Schedule with EventBridge on day 1 of each month. The function lists
services above $100 of UnblendedCost for the previous full month —
adjust TimePeriod or compute it dynamically for the trailing month.
"""

import boto3

ce = boto3.client("ce")


def lambda_handler(event, context):
    response = ce.get_cost_and_usage(
        TimePeriod={"Start": "2026-06-01", "End": "2026-07-01"},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "SERVICE", "Key": "Service"}],
    )

    costs = []
    for group in response["ResultsByTime"][0]["Groups"]:
        service = group["Keys"][0]
        amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
        if amount > 100:
            costs.append(f"{service}: ${amount:.2f}")

    if costs:
        send_slack_notification("\n".join(costs))  # your webhook helper

    return {"statusCode": 200}


def send_slack_notification(text):
    raise NotImplementedError("post to your Slack incoming webhook")
