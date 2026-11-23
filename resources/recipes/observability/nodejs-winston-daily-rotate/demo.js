// Writes a burst of log entries so you can see rotation files appear in logs/.
import logger from "./logger.js";

for (let i = 0; i < 100; i++) {
  logger.info("demo_event", { iteration: i, payload: "x".repeat(200) });
}
logger.warn("demo_warning", { note: "half-way through" });
logger.error("demo_error", { error: new Error("demo boom") });

console.log("Wrote 102 log entries — check logs/");
