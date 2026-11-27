import { DynamoDBClient, UpdateItemCommand, GetItemCommand } from '@aws-sdk/client-dynamodb';
import { marshall, unmarshall } from '@aws-sdk/util-dynamodb';

const ddb = new DynamoDBClient({ region: 'us-east-1' });

export class TokenBucket {
  private tableName = 'rate_limits';
  constructor(private capacity: number, private refillRate: number) {}

  async allowRequest(bucketKey: string, tokens = 1): Promise<boolean> {
    const now = Date.now();
    const getResponse = await ddb.send(new GetItemCommand({
      TableName: this.tableName,
      Key: marshall({ bucketKey }),
    }));

    let tokensAvailable = this.capacity;
    let lastRefill = now;

    if (getResponse.Item) {
      const bucket = unmarshall(getResponse.Item);
      tokensAvailable = parseFloat(bucket.tokens);
      lastRefill = parseInt(bucket.lastRefill);
      const elapsedSeconds = (now - lastRefill) / 1000;
      tokensAvailable = Math.min(this.capacity, tokensAvailable + elapsedSeconds * this.refillRate);
    }

    if (tokensAvailable < tokens) return false;

    await ddb.send(new UpdateItemCommand({
      TableName: this.tableName,
      Key: marshall({ bucketKey }),
      UpdateExpression: 'SET tokens = :t, lastRefill = :r',
      ExpressionAttributeValues: marshall({
        ':t': (tokensAvailable - tokens).toFixed(2),
        ':r': now.toString(),
      }),
    }));

    return true;
  }
}

const rateLimiter = new TokenBucket(100, 10);

export const handler = async (event: any): Promise<{ statusCode: number }> => {
  const apiKey = event.requestContext.identity.apiId;
  if (!(await rateLimiter.allowRequest(apiKey))) {
    return { statusCode: 429, body: JSON.stringify({ error: 'Rate limit exceeded' }) };
  }
  return { statusCode: 200 };
};
