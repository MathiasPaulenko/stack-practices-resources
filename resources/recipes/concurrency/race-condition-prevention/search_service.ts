// Pattern 1: cancel the previous request before firing a new one.
// The stale fetch is aborted mid-flight instead of racing the latest query.
class SearchService {
  private abortController: AbortController | null = null;

  async search(query: string): Promise<unknown[]> {
    this.abortController?.abort();
    this.abortController = new AbortController();

    const response = await fetch(`/api/search?q=${query}`, {
      signal: this.abortController.signal,
    });

    return response.json();
  }
}
