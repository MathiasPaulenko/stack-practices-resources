// Pattern 3: latest-only execution. Each call stamps a request id; a response
// whose id was superseded is discarded instead of rendered.
import { useCallback, useRef } from 'react';

function useLatestQuery<T>() {
  const latestRequest = useRef(0);

  return useCallback(
    async (query: string, fetcher: (q: string) => Promise<T>): Promise<T> => {
      const requestId = ++latestRequest.current;
      const result = await fetcher(query);

      if (requestId !== latestRequest.current) {
        throw new Error('Stale request');
      }

      return result;
    },
    []
  );
}
