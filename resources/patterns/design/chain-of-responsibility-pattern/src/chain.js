// Chain of Responsibility Pattern — runnable demo
// Usage: node chain.js
class Handler {
  constructor() { this.nextHandler = null; }
  setNext(handler) { this.nextHandler = handler; return handler; }
  handle(request) {
    if (this.nextHandler) return this.nextHandler.handle(request);
    return null;
  }
}
class AuthHandler extends Handler {
  handle(request) {
    if (!request.startsWith("token:")) return "401 Unauthorized";
    return super.handle(request);
  }
}
class RateLimitHandler extends Handler {
  constructor() { super(); this.requests = 0; this.limit = 3; }
  handle(request) {
    this.requests++;
    if (this.requests > this.limit) return "429 Too Many Requests";
    return super.handle(request);
  }
}
class DataHandler extends Handler {
  handle(request) { return `Processed: ${request}`; }
}
const handler = new AuthHandler();
handler.setNext(new RateLimitHandler()).setNext(new DataHandler());
console.log(handler.handle("token:abc123"));
console.log(handler.handle("bad-request"));
