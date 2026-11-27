// Warmup Lambda handler (TypeScript / AWS SDK v3).
// Sends WARM_COUNT concurrent async invocations to TARGET_FUNCTION so Lambda
// keeps that many execution environments warm.
import { LambdaClient, InvokeCommand } from '@aws-sdk/client-lambda';

const lambdaClient = new LambdaClient({ region: 'us-east-1' });

const TARGET_FUNCTION = process.env.TARGET_FUNCTION!;
const WARM_COUNT = parseInt(process.env.WARM_COUNT || '5');

export const handler = async (): Promise<{ warmedInstances: number }> => {
  const promises = Array.from({ length: WARM_COUNT }, (_, i) =>
    lambdaClient.send(new InvokeCommand({
      FunctionName: TARGET_FUNCTION,
      InvocationType: 'Event', // Async
      Payload: JSON.stringify({
        source: 'warmup.ping',
        instanceId: i,
        isWarmup: true,
      }),
    }))
  );

  const results = await Promise.all(promises);

  return {
    warmedInstances: results.length,
  };
};
