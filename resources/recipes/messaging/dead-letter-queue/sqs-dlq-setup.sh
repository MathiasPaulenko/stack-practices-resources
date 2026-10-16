#!/usr/bin/env bash
# SQS dead-letter queue setup: main queue + DLQ + redrive policy.
# Requires AWS CLI configured with sqs:CreateQueue / SetQueueAttributes permissions.
set -euo pipefail

# Create the main queue and its DLQ
aws sqs create-queue --queue-name orders-queue
aws sqs create-queue --queue-name orders-dlq

# Resolve URLs and the DLQ ARN
QUEUE_URL=$(aws sqs get-queue-url --queue-name orders-queue --query 'QueueUrl' --output text)
DLQ_URL=$(aws sqs get-queue-url --queue-name orders-dlq --query 'QueueUrl' --output text)
DLQ_ARN=$(aws sqs get-queue-attributes --queue-url "$DLQ_URL" \
  --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

# Send a message to the DLQ after 3 failed receives
aws sqs set-queue-attributes \
  --queue-url "$QUEUE_URL" \
  --attributes "{
    \"RedrivePolicy\": \"{\\\"deadLetterTargetArn\\\":\\\"$DLQ_ARN\\\",\\\"maxReceiveCount\\\":3}\"
  }"

echo "Redrive policy set: orders-queue -> orders-dlq (maxReceiveCount=3)"
