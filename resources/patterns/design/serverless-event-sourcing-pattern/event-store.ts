// Event store on DynamoDB with EventBridge fan-out (TypeScript).
//
// Appends an event to the event_store table and publishes it to EventBridge
// so downstream consumers react without coupling to the write side.
// Deps: @aws-sdk/client-dynamodb, @aws-sdk/client-eventbridge,
//       @aws-sdk/util-dynamodb

import { DynamoDBClient, PutItemCommand, QueryCommand } from '@aws-sdk/client-dynamodb';
import { EventBridgeClient, PutEventsCommand } from '@aws-sdk/client-eventbridge';
import { marshall, unmarshall } from '@aws-sdk/util-dynamodb';

const ddb = new DynamoDBClient({});
const eventBridge = new EventBridgeClient({});

interface DomainEvent {
  aggregateId: string;
  eventId: string;
  eventType: string;
  data: Record<string, any>;
  timestamp: number;
  version: number;
}

class EventStore {
  private tableName = 'event_store';

  async append(aggregateId: string, eventType: string, data: Record<string, any>): Promise<DomainEvent> {
    const version = await this.getNextVersion(aggregateId);
    const event: DomainEvent = {
      aggregateId,
      eventId: crypto.randomUUID(),
      eventType,
      data,
      timestamp: Date.now(),
      version,
    };

    await ddb.send(new PutItemCommand({
      TableName: this.tableName,
      Item: marshall(event),
    }));

    await eventBridge.send(new PutEventsCommand({
      Entries: [{
        EventBusName: 'default',
        Source: 'order.service',
        DetailType: eventType,
        Detail: JSON.stringify(event),
      }],
    }));

    return event;
  }

  async getEvents(aggregateId: string, fromVersion = 0): Promise<DomainEvent[]> {
    const response = await ddb.send(new QueryCommand({
      TableName: this.tableName,
      KeyConditionExpression: 'aggregateId = :id AND #v >= :v',
      ExpressionAttributeNames: { '#v': 'version' },
      ExpressionAttributeValues: marshall({ ':id': aggregateId, ':v': fromVersion }),
      ScanIndexForward: true,
    }));

    return (response.Items || []).map(item => unmarshall(item) as DomainEvent);
  }

  private async getNextVersion(aggregateId: string): Promise<number> {
    const response = await ddb.send(new QueryCommand({
      TableName: this.tableName,
      KeyConditionExpression: 'aggregateId = :id',
      ExpressionAttributeValues: marshall({ ':id': aggregateId }),
      ScanIndexForward: false,
      Limit: 1,
    }));

    const items = response.Items || [];
    return items.length > 0 ? unmarshall(items[0]).version + 1 : 1;
  }
}

const store = new EventStore();

// Rebuild state by replaying the log for one aggregate.
function replayEvents(events: DomainEvent[]): Record<string, any> {
  return events.reduce((state, event) => ({
    ...state,
    ...event.data,
    version: event.version,
  }), {});
}

export { EventStore, replayEvents };
