import { DynamoDBStreamEvent } from 'aws-lambda';
import { unmarshall } from '@aws-sdk/util-dynamodb';
import type { DomainEvent } from './eventstore';

/**
 * Lambda triggered by a DynamoDB Stream. Each INSERT record is a newly
 * appended domain event; the handler routes it to the right projection.
 *
 * Idempotency note: streams are at-least-once, so a record can be
 * delivered more than once. Make every projection update idempotent —
 * e.g. store eventId on the projection row and skip if already applied.
 */
export const handler = async (event: DynamoDBStreamEvent): Promise<void> => {
  for (const record of event.Records) {
    if (record.eventName !== 'INSERT') continue;

    const newImage = unmarshall(record.dynamodb!.NewImage!);
    const domainEvent: DomainEvent = {
      eventId: newImage.eventId,
      aggregateId: newImage.aggregateId,
      eventType: newImage.eventType,
      payload: newImage.payload,
      timestamp: newImage.timestamp,
      version: newImage.version,
    };

    await projectEvent(domainEvent);
  }
};

async function projectEvent(event: DomainEvent): Promise<void> {
  switch (event.eventType) {
    case 'OrderCreated':
      await createOrderProjection(event.aggregateId, event.payload);
      break;
    case 'ItemAdded':
      await addItemToOrderProjection(event.aggregateId, event.payload);
      break;
    case 'OrderShipped':
      await updateOrderStatus(event.aggregateId, 'shipped');
      break;
  }
}

// --- projection writers: implement against your read model store ---

async function createOrderProjection(
  orderId: string,
  payload: Record<string, unknown>,
): Promise<void> {
  // insert a new row into the read-optimized orders table
  void orderId; void payload;
}

async function addItemToOrderProjection(
  orderId: string,
  payload: Record<string, unknown>,
): Promise<void> {
  // append item + recompute denormalized totals on the read row
  void orderId; void payload;
}

async function updateOrderStatus(
  orderId: string,
  status: string,
): Promise<void> {
  // patch the status column of the projection row
  void orderId; void status;
}
