// Null Object pattern in JavaScript: Logger/Config null objects + OrderService.

class ConsoleLogger {
  info(msg) { console.log(`[INFO] ${msg}`); }
  warn(msg) { console.warn(`[WARN] ${msg}`); }
  error(msg) { console.error(`[ERROR] ${msg}`); }
  debug(msg) { console.log(`[DEBUG] ${msg}`); }
}

// Null object: same interface, does nothing.
class NullLogger {
  info(_msg) {}
  warn(_msg) {}
  error(_msg) {}
  debug(_msg) {}
}

class EnvConfig {
  get(key) { return process.env[key]; }
  getNumber(key) { const v = Number(process.env[key]); return Number.isNaN(v) ? undefined : v; }
  getBoolean(key) { return process.env[key] === 'true'; }
}

class NullConfig {
  get(_key) { return undefined; }
  getNumber(_key) { return undefined; }
  getBoolean(_key) { return false; }
}

class OrderService {
  constructor(logger, config) {
    this.logger = logger;
    this.config = config;
  }

  process(order) {
    this.logger.info(`Processing order ${order.id}`);
    const maxItems = this.config.getNumber('MAX_ITEMS') || 100;
    if (order.items.length > maxItems) {
      this.logger.warn(`Order ${order.id} exceeds max items`);
    }
  }
}

const order = { id: 42, items: ['a', 'b', 'c'] };

// "Test" run: silence, no errors — no mock framework needed.
const testService = new OrderService(new NullLogger(), new NullConfig());
testService.process(order);
console.log('test run: silent, no errors');

// "Production" run: real collaborators.
const prodService = new OrderService(new ConsoleLogger(), new EnvConfig());
prodService.process(order);
