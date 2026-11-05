// middleware.ts — Correlation ID middleware for Express
import { randomUUID } from "crypto";
import type { NextFunction, Request, Response } from "express";
import { asyncLocalStorage, logger } from "./logger";

export function correlationIdMiddleware(
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const requestId = (req.headers["x-request-id"] as string) || randomUUID();
  const userId = (req as any).user?.id;

  res.setHeader("X-Request-ID", requestId);
  const startedAt = Date.now();

  asyncLocalStorage.run({ requestId, userId }, () => {
    logger.info("request_started", {
      method: req.method,
      url: req.originalUrl,
    });

    res.on("finish", () => {
      logger.info("request_completed", {
        method: req.method,
        url: req.originalUrl,
        status: res.statusCode,
        duration_ms: Date.now() - startedAt,
      });
    });

    next();
  });
}
