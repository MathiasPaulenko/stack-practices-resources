// API Lambda handler with warmup detection (TypeScript).
// Checks for the `isWarmup` flag first and returns immediately so ping
// invocations keep the environment alive without triggering business logic.
interface WarmupEvent {
  source: string;
  instanceId: number;
  isWarmup: boolean;
}

interface ApiEvent {
  httpMethod: string;
  path: string;
  body?: string;
}

type HandlerResult =
  | { status: string; instanceId: number }
  | { statusCode: number; body: string };

export const handler = async (event: WarmupEvent | ApiEvent): Promise<HandlerResult> => {
  // Detect warmup ping
  if ('isWarmup' in event && event.isWarmup) {
    return { status: 'warm', instanceId: event.instanceId };
  }

  // Real request processing
  const { httpMethod, path } = event as ApiEvent;

  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Request processed', path }),
  };
};
