import { BaseClientDecorator } from './BaseClientDecorator.js';
import type { HttpClient } from './HttpClient.js';

export class AuthDecorator extends BaseClientDecorator {
  constructor(client: HttpClient, private token: string) {
    super(client);
  }

  async request(url: string, options: RequestInit): Promise<Response> {
    const headers = new Headers(options.headers);
    headers.set('Authorization', `Bearer ${this.token}`);
    return this.client.request(url, { ...options, headers });
  }
}
