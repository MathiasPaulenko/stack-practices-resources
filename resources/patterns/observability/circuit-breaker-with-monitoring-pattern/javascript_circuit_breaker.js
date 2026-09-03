const { CircuitBreaker } = require("opossum");
const promClient = require("prom-client");

function createMonitoredBreaker(name, endpoint, fn, options = {}, register) {
  const registry = register || new promClient.Registry();

  const circuitState = new promClient.Gauge({
    name: "circuit_breaker_state",
    help: "Circuit breaker state (0=closed, 1=open, 2=half_open)",
    labelNames: ["service", "endpoint"],
    registers: [registry],
  });

  const circuitFailures = new promClient.Counter({
    name: "circuit_breaker_failures_total",
    help: "Total failures",
    labelNames: ["service", "endpoint"],
    registers: [registry],
  });

  const circuitRejected = new promClient.Counter({
    name: "circuit_breaker_rejected_total",
    help: "Total rejected calls",
    labelNames: ["service", "endpoint"],
    registers: [registry],
  });

  const circuitTransitions = new promClient.Counter({
    name: "circuit_breaker_state_transitions_total",
    help: "State transitions",
    labelNames: ["service", "endpoint", "from_state", "to_state"],
    registers: [registry],
  });

  const breaker = new CircuitBreaker(fn, {
    timeout: options.timeout || 5000,
    errorThresholdPercentage: options.errorThreshold || 50,
    resetTimeout: options.resetTimeout || 30000,
    rollingCountTimeout: 60000,
    rollingCountBuckets: 10,
    name: `${name}/${endpoint}`,
  });

  const labels = { service: name, endpoint };
  const stateMap = { closed: 0, opened: 1, halfOpen: 2 };

  breaker.on("state", (from, to) => {
    circuitState.labels(labels).set(stateMap[to] ?? 0);
    circuitTransitions.labels({ ...labels, from_state: from, to_state: to }).inc();
  });

  breaker.on("failure", () => circuitFailures.labels(labels).inc());
  breaker.on("reject", () => circuitRejected.labels(labels).inc());

  circuitState.labels(labels).set(0);

  return { breaker, registry };
}

module.exports = { createMonitoredBreaker };
