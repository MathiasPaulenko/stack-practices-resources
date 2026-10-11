import { DynamoDBDocument } from '@aws-sdk/lib-dynamodb';

export interface DomainEvent {
  eventId: string;
  aggregateId: string;
  eventType: string;
  payload: Record<string, unknown>;
  timestamp: string;
  version: number;
}

/**
 * Append-only event store backed by DynamoDB.
 * Partition key: ORDER#<aggregateId>, sort key: EVENT#<padded version>.
 * ConditionExpression guards optimistic concurrency — concurrent appends
 * to the same aggregate fail instead of silently overwriting.
 */
export class OrderEventStore {
  constructor(private tableName: string, private client: DynamoDBDocument) {}

  async appendEvents(aggregateId: string, events: DomainEvent[]): Promise<void> {
    const currentVersion = await this.getCurrentVersion(aggregateId);

    const transactItems = events.map((event, index) => ({
      Put: {
        TableName: this.tableName,
        Item: {
          pk: `ORDER#${aggregateId}`,
          sk: `EVENT#${(currentVersion + index + 1).toString().padStart(10, '0')}`,
          eventId: event.eventId,
          eventType: event.eventType,
          payload: event.payload,
          timestamp: new Date().toISOString(),
          version: currentVersion + index + 1,
        },
        ConditionExpression: 'attribute_not_exists(pk)',
      },
    }));

    await this.client.transactWrite({ TransactItems: transactItems });
  }

  async getEvents(aggregateId: string): Promise<DomainEvent[]> {
    const result = await this.client.query({
      TableName: this.tableName,
      KeyConditionExpression: 'pk = :pk AND begins_with(sk, :sk)',
      ExpressionAttributeValues: {
        ':pk': `ORDER#${aggregateId}`,
        ':sk': 'EVENT#',
      },
      ScanIndexForward: true,
    });

    return (result.Items || []).map(item => ({
      eventId: item.eventId as string,
      aggregateId,
      eventType: item.eventType as string,
      payload: item.payload as Record<string, unknown>,
      timestamp: item.timestamp as string,
      version: item.version as number,
    }));
  }

  private async getCurrentVersion(aggregateId: string): Promise<number> {
    const events = await this.getEvents(aggregateId);
    return events.length > 0 ? events[events.length - 1].version : 0;
  }
}
