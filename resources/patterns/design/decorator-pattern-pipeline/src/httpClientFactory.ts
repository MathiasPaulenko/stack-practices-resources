import type { HttpClient } from './HttpClient.js';
import { FetchClient } from './FetchClient.js';
import { LoggingDecorator } from './LoggingDecorator.js';
import { RetryDecorator } from './RetryDecorator.js';
import { AuthDecorator } from './AuthDecorator.js';
import { CircuitBreakerDecorator } from './CircuitBreakerDecorator.js';

export function createHttpClient(config: {
  token: string;
  maxRetries?: number;
  timeoutMs?: number;
}): HttpClient {
  let client: HttpClient = new FetchClient();
  client = new CircuitBreakerDecorator(client);
  client = new LoggingDecorator(client);
  client = new RetryDecorator(client, config.maxRetries ?? 3);
  client = new AuthDecorator(client, config.token);
  return client;
}
