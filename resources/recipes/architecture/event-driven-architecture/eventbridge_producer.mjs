#!/usr/bin/env node
// Publish to AWS EventBridge and consume from the SQS target.
import {
  EventBridgeClient,
  PutEventsCommand,
} from "@aws-sdk/client-eventbridge";
import {
  SQSClient,
  ReceiveMessageCommand,
  DeleteMessageCommand,
} from "@aws-sdk/client-sqs";

const eventBridge = new EventBridgeClient({ region: "us-east-1" });
const sqs = new SQSClient({ region: "us-east-1" });

// Publishing to EventBridge
export async function publishOrderEvent(order) {
  const command = new PutEventsCommand({
    Entries: [
      {
        EventBusName: "stackpractices-events",
        Source: "order-service",
        DetailType: "OrderPlaced",
        Detail: JSON.stringify({
          orderId: order.id,
          customerId: order.customerId,
          total: order.total,
          items: order.items,
        }),
      },
    ],
  });
  await eventBridge.send(command);
}

// Consuming from SQS (EventBridge target)
export async function processOrderEvents() {
  const result = await sqs.send(
    new ReceiveMessageCommand({
      QueueUrl: process.env.INVENTORY_QUEUE_URL,
      MaxNumberOfMessages: 10,
      WaitTimeSeconds: 20,
    })
  );

  for (const message of result.Messages || []) {
    try {
      const event = JSON.parse(message.Body);
      const detail = JSON.parse(event.detail);

      await reserveInventory(detail.items);
      await sqs.send(
        new DeleteMessageCommand({
          QueueUrl: process.env.INVENTORY_QUEUE_URL,
          ReceiptHandle: message.ReceiptHandle,
        })
      );
    } catch (error) {
      // Message becomes visible again after the visibility timeout;
      // after max retries it moves to the DLQ
      console.error("Failed to process order event:", error);
    }
  }
}

async function reserveInventory(items) {
  throw new Error("Provide your own inventory service");
}
