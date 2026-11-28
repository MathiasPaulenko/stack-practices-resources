class SlidingWindowThrottle {
  constructor(windowMs, maxRequests) {
    this.windowMs = windowMs;
    this.maxRequests = maxRequests;
    this.requests = new Map();
  }

  isAllowed(clientId) {
    const now = Date.now();
    const windowStart = now - this.windowMs;
    const clientRequests = (this.requests.get(clientId) || [])
      .filter(t => t > windowStart);

    if (clientRequests.length >= this.maxRequests) {
      this.requests.set(clientId, clientRequests);
      return false;
    }
    clientRequests.push(now);
    this.requests.set(clientId, clientRequests);
    return true;
  }
}
