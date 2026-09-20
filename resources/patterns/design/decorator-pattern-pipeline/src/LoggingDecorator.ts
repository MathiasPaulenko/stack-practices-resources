import { BaseClientDecorator } from './BaseClientDecorator.js';

export class LoggingDecorator extends BaseClientDecorator {
  async request(url: string, options: RequestInit): Promise<Response> {
    const start = performance.now();
    try {
      const response = await this.client.request(url, options);
      console.log(
        `${options.method || 'GET'} ${url} → ${response.status} (${(performance.now() - start).toFixed(0)}ms)`
      );
      return response;
    } catch (error) {
      console.error(`${options.method || 'GET'} ${url} → ERROR`);
      throw error;
    }
  }
}
