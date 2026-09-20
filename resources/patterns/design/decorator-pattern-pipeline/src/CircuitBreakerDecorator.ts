import { BaseClientDecorator } from './BaseClientDecorator.js';
import type { HttpClient } from './HttpClient.js';

export class CircuitBreakerDecorator extends BaseClientDecorator {
  private failures = 0;
  private isOpen = false;
  private halfOpen = false;
  private openedAt = 0;

  constructor(
    client: HttpClient,
    private threshold: number = 5,
    private resetTimeout: number = 30000
  ) {
    super(client);
  }

  async request(url: string, options: RequestInit): Promise<Response> {
    if (this.isOpen) {
      if (Date.now() - this.openedAt > this.resetTimeout) {
        this.isOpen = false;
        this.halfOpen = true; // allow one probe request
      } else {
        throw new Error(`Circuit breaker open for ${url}`);
      }
    }

    try {
      const response = await this.client.request(url, options);
      if (response.ok) {
        this.failures = 0;
        this.halfOpen = false;
      } else {
        this.recordFailure();
      }
      return response;
    } catch (error) {
      this.recordFailure();
      throw error;
    }
  }

  private recordFailure(): void {
    this.failures++;
    if (this.halfOpen || this.failures >= this.threshold) {
      this.isOpen = true;
      this.halfOpen = false;
      this.openedAt = Date.now();
    }
  }
}
