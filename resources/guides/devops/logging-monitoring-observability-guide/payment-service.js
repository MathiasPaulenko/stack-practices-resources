// OpenTelemetry instrumentation for a payment service (Node.js).
// Companion to stackpractices.com/guides/logging-monitoring-observability-guide/
//
// Requires:
//   npm install @opentelemetry/api @opentelemetry/sdk-node
//     @opentelemetry/auto-instrumentations-node
//     @opentelemetry/exporter-trace-otlp-grpc
//     @opentelemetry/exporter-metrics-otlp-grpc
//
// The OTel Collector endpoint defaults to http://localhost:4317 (docker-compose lab).

const { trace, metrics, SpanStatusCode } = require("@opentelemetry/api");

const tracer = trace.getTracer("payment-service");
const meter = metrics.getMeter("payment-service");
const paymentsTotal = meter.createCounter("payments.total");
const paymentsErrors = meter.createCounter("payments.errors");

async function processPayment(payment, gateway) {
  const span = tracer.startSpan("processPayment");
  span.setAttribute("payment.amount", payment.amount);
  span.setAttribute("payment.currency", payment.currency);
  try {
    const result = await gateway.charge(payment);
    span.setAttribute("payment.status", result.status);
    paymentsTotal.add(1, { status: result.status, gateway: "stripe" });
    return result;
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
    paymentsErrors.add(1, { type: error.constructor.name });
    throw error;
  } finally {
    span.end();
  }
}

module.exports = { processPayment };
