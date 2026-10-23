import { EventBridgeClient, PutEventsCommand } from "@aws-sdk/client-eventbridge";
import { randomUUID } from "node:crypto";

const eb = new EventBridgeClient({ region: "us-east-1" });

export async function publishOrderPlaced(order) {
  await eb.send(
    new PutEventsCommand({
      Entries: [
        {
          Source: "order-service",
          DetailType: "OrderPlaced",
          Detail: JSON.stringify({
            eventId: randomUUID(), // consumers dedupe on this
            orderId: order.id,
            amount: order.total,
            customerEmail: order.email,
          }),
        },
      ],
    })
  );
}

// node publisher.mjs  →  send one test event
if (import.meta.url === `file://${process.argv[1]}`) {
  await publishOrderPlaced({ id: "ord-1001", total: 49.99, email: "test@example.com" });
  console.log("OrderPlaced event sent");
}
