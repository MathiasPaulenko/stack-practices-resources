import { BaseClientDecorator } from './BaseClientDecorator.js';
import type { HttpClient } from './HttpClient.js';

export class RetryDecorator extends BaseClientDecorator {
  private static readonly retryableStatuses = new Set([502, 503, 504]);

  constructor(
    client: HttpClient,
    private maxRetries: number = 3,
    private baseDelayMs: number = 500
  ) {
    super(client);
  }

  async request(url: string, options: RequestInit): Promise<Response> {
    let lastError: unknown;
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        const response = await this.client.request(url, options);
        // fetch only throws on network errors — HTTP failures need checking
        if (response.ok || !RetryDecorator.retryableStatuses.has(response.status)) {
          return response;
        }
        lastError = new Error(`HTTP ${response.status} from ${url}`);
      } catch (error) {
        lastError = error; // network error: retryable
      }
      if (attempt < this.maxRetries) {
        // exponential backoff with jitter avoids synchronized retries
        const delay = this.baseDelayMs * 2 ** attempt + Math.random() * 100;
        await new Promise(r => setTimeout(r, delay));
      }
    }
    throw lastError;
  }
}
