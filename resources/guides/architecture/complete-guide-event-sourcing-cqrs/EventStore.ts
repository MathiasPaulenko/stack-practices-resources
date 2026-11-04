// EventStore.ts — Append-only event storage with optimistic concurrency
interface DomainEvent {
  eventId: string;
  eventType: string;
  aggregateId: string;
  aggregateType: string;
  data: Record<string, any>;
  metadata: Record<string, any>;
  version: number;
  timestamp: Date;
}

class PostgresEventStore {
  constructor(private readonly pool: Pool) {}

  async append(aggregateId: string, events: DomainEvent[], expectedVersion: number): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      const currentVersion = await this.getCurrentVersion(client, aggregateId);
      if (currentVersion !== expectedVersion) {
        throw new ConcurrencyError(`Expected version ${expectedVersion}, got ${currentVersion}`);
      }
      for (let i = 0; i < events.length; i++) {
        const event = events[i];
        event.version = expectedVersion + i + 1;
        await client.query(
          `INSERT INTO events (event_id, event_type, aggregate_id, aggregate_type, event_data, metadata, version, timestamp)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
          [event.eventId, event.eventType, event.aggregateId, event.aggregateType,
           JSON.stringify(event.data), JSON.stringify(event.metadata), event.version, event.timestamp],
        );
      }
      await client.query('COMMIT');
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  async getEvents(aggregateId: string, fromVersion = 0): Promise<DomainEvent[]> {
    const result = await this.pool.query(
      `SELECT * FROM events WHERE aggregate_id = $1 AND version > $2 ORDER BY version ASC`,
      [aggregateId, fromVersion],
    );
    return result.rows;
  }

  private async getCurrentVersion(client: PoolClient, aggregateId: string): Promise<number> {
    const result = await client.query(
      `SELECT COALESCE(MAX(version), 0) as version FROM events WHERE aggregate_id = $1`,
      [aggregateId],
    );
    return result.rows[0].version;
  }
}
