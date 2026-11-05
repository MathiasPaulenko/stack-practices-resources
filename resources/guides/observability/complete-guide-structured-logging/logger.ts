// logger.ts — pino structured logging
import pino from "pino";
import { AsyncLocalStorage } from "async_hooks";

export const asyncLocalStorage = new AsyncLocalStorage<{
  requestId: string;
  userId?: string;
  traceId?: string;
}>();

export const logger = pino({
  level: process.env.LOG_LEVEL || "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
  mixin: () => {
    const store = asyncLocalStorage.getStore();
    return store ? { ...store } : {};
  },
  timestamp: pino.stdTimeFunctions.isoTime,
  redact: {
    paths: ["password", "token", "authorization", "*.password"],
    censor: "[REDACTED]",
  },
});
