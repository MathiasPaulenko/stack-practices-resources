import type { HttpClient } from './HttpClient.js';

export abstract class BaseClientDecorator implements HttpClient {
  constructor(protected client: HttpClient) {}
  abstract request(url: string, options: RequestInit): Promise<Response>;
}
