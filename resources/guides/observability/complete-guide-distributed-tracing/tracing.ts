// tracing.ts — OpenTelemetry setup for Node.js services.
import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-grpc";
import { Resource } from "@opentelemetry/resources";
import { ATTR_SERVICE_NAME, ATTR_SERVICE_VERSION } from "@opentelemetry/semantic-conventions";
import { ExpressInstrumentation } from "@opentelemetry/instrumentation-express";
import { HttpInstrumentation } from "@opentelemetry/instrumentation-http";
import { PgInstrumentation } from "@opentelemetry/instrumentation-pg";
import { RedisInstrumentation } from "@opentelemetry/instrumentation-redis-4";
import { trace, context, SpanStatusCode } from "@opentelemetry/api";

export function startTracing(): NodeSDK {
  const sdk = new NodeSDK({
    resource: new Resource({
      [ATTR_SERVICE_NAME]: "api-gateway",
      [ATTR_SERVICE_VERSION]: "1.0.0",
    }),
    traceExporter: new OTLPTraceExporter({
      url: "http://otel-collector:4317",
    }),
    instrumentations: [
      new HttpInstrumentation(),
      new ExpressInstrumentation(),
      new PgInstrumentation(),
      new RedisInstrumentation(),
    ],
  });
  sdk.start();
  return sdk;
}

const tracer = trace.getTracer("api-gateway");

export async function handleRequest(req: any, res: any): Promise<void> {
  const span = tracer.startSpan("handle_request", {
    attributes: {
      "http.method": req.method,
      "http.url": req.url,
      "user.id": req.userId,
    },
  });

  try {
    await context.with(trace.setSpan(context.active(), span), async () => {
      const authResult = await validateToken(req.headers.authorization);
      const userData = await fetchUserData(req.userId);
      const processedData = await processData(userData);

      span.setAttribute("response.size", JSON.stringify(processedData).length);
      span.setStatus({ code: SpanStatusCode.OK });
      res.json(processedData);
    });
  } catch (error: any) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
    res.status(500).json({ error: "Internal server error" });
  } finally {
    span.end();
  }
}

declare function validateToken(token?: string): Promise<unknown>;
declare function fetchUserData(userId: string): Promise<unknown>;
declare function processData(data: unknown): Promise<unknown>;
