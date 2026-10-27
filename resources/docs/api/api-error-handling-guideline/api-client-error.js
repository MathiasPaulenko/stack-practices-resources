async function callApi(path) {
  const res = await fetch(path);
  if (res.ok) return res.json();

  const { error } = await res.json().catch(() => ({}));
  const apiError = new ApiClientError(
    error?.code ?? 'UNKNOWN',
    error?.message ?? `HTTP ${res.status}`,
    { id: error?.id, retryable: error?.retryable ?? res.status >= 500 },
  );

  if (apiError.retryable) throw apiError;
  if (apiError.code === 'RATE_LIMIT_EXCEEDED') {
    const wait = Number(res.headers.get('Retry-After') ?? 5) * 1000;
    await new Promise(r => setTimeout(r, wait));
    return callApi(path);
  }
  throw apiError;
}
