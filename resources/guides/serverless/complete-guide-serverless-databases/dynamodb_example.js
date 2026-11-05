// Companion: DynamoDB order service — access-pattern-first design
// Requires: npm install @aws-sdk/client-dynamodb  +  AWS credentials
import { DynamoDBClient, PutItemCommand, QueryCommand } from '@aws-sdk/client-dynamodb';
const client = new DynamoDBClient({});

// Schema designed around the query: pk=user#<id>, sk=order#<date>
export async function createOrder(userId, orderId, total) {
  await client.send(new PutItemCommand({
    TableName: 'orders',
    Item: {
      pk: { S: `user#${userId}` },
      sk: { S: `order#${orderId}` },
      total: { N: String(total) },
    },
  }));
}

export async function getUserOrders(userId) {
  const res = await client.send(new QueryCommand({
    TableName: 'orders',
    KeyConditionExpression: 'pk = :pk AND begins_with(sk, :p)',
    ExpressionAttributeValues: {
      ':pk': { S: `user#${userId}` },
      ':p': { S: 'order#' },
    },
  }));
  return res.Items;
}
