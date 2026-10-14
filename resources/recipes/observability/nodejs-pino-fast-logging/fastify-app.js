// Fastify ships with pino built in — pass logger options directly.
const fastify = require("fastify")({
  logger: {
    level: process.env.LOG_LEVEL || "info",
    transport:
      process.env.NODE_ENV === "development"
        ? { target: "pino-pretty", options: { colorize: true, ignore: "pid,hostname" } }
        : undefined,
  },
});

fastify.get("/api/users/:id", async (request) => {
  request.log.info({ user_id: request.params.id }, "fetching_user");
  return { id: request.params.id, name: "Alice" };
});

fastify.listen({ port: 3001 });
