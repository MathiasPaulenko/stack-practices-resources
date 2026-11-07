import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Fetches `url` and exposes { data, loading, error, refetch }.
 * A null/empty url makes the hook a no-op — used for the `enabled` pattern.
 * `options` is read through a ref so a fresh options object per render
 * does not trigger a refetch.
 */
export function useFetch(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(!!url);
  const [error, setError] = useState(null);
  const optionsRef = useRef(options);

  const fetchData = useCallback(async () => {
    if (!url) {
      setData(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(url, optionsRef.current);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const json = await response.json();
      setData(json);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

export default useFetch;
