import type { HttpClient } from './HttpClient.js';

export class FetchClient implements HttpClient {
  async request(url: string, options: RequestInit): Promise<Response> {
    return fetch(url, options);
  }
}
