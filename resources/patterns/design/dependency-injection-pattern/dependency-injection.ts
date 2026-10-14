/**
 * Dependency Injection: manual constructor injection plus a tiny container.
 *
 * Shows both ends of the pattern — plain constructor wiring (all you need
 * for small apps) and a minimal container that resolves a dependency graph
 * automatically (the shape of what tsyringe/InversifyJS do at scale).
 *
 * No dependencies; run with: npx tsx dependency-injection.ts
 */

interface PaymentProcessor {
  charge(amount: number): boolean;
}

class StripeProcessor implements PaymentProcessor {
  charge(amount: number): boolean {
    console.log(`Charging $${amount} via Stripe`);
    return true;
  }
}

interface Logger {
  log(msg: string): void;
}

class ConsoleLogger implements Logger {
  log(msg: string): void {
    console.log(`[log] ${msg}`);
  }
}

class OrderService {
  // Dependencies arrive through the constructor — nothing is created here.
  constructor(
    private readonly processor: PaymentProcessor,
    private readonly logger: Logger,
  ) {}

  checkout(amount: number): boolean {
    const ok = this.processor.charge(amount);
    this.logger.log(`checkout(${amount}) -> ${ok}`);
    return ok;
  }
}

// --- Manual wiring at the composition root (the default choice) ---

function compositionRoot(): OrderService {
  return new OrderService(new StripeProcessor(), new ConsoleLogger());
}

// --- A minimal DI container: register a factory per token, resolve lazily ---

type Token<T> = abstract new (...args: never[]) => T | (new (...args: never[]) => T);

class Container {
  private factories = new Map<Token<unknown>, (c: Container) => unknown>();
  private singletons = new Map<Token<unknown>, unknown>();

  register<T>(token: Token<T>, factory: (c: Container) => T, opts: { singleton?: boolean } = {}): void {
    this.factories.set(token, opts.singleton
      ? (c) => {
          if (!this.singletons.has(token)) this.singletons.set(token, factory(c));
          return this.singletons.get(token);
        }
      : factory);
  }

  resolve<T>(token: Token<T>): T {
    const factory = this.factories.get(token);
    if (!factory) throw new Error(`No registration for ${(token as Function).name}`);
    return factory(this) as T;
  }
}

// Token interfaces need runtime handles — use abstract classes as tokens.
abstract class PaymentProcessorToken implements PaymentProcessor {
  abstract charge(amount: number): boolean;
}
abstract class LoggerToken implements Logger {
  abstract log(msg: string): void;
}

function containerRoot(): OrderService {
  const c = new Container();
  c.register<Logger>(LoggerToken, () => new ConsoleLogger(), { singleton: true });
  c.register<PaymentProcessor>(PaymentProcessorToken, () => new StripeProcessor(), { singleton: true });
  c.register<OrderService>(OrderService, (c) => new OrderService(c.resolve(PaymentProcessorToken), c.resolve(LoggerToken)));
  return c.resolve(OrderService);
}

compositionRoot().checkout(100.0);
containerRoot().checkout(42.5);

// Scope demo: singleton shares one instance, transient builds a new one.
const scoped = new Container();
scoped.register<Logger>(LoggerToken, () => new ConsoleLogger(), { singleton: true });
scoped.register<OrderService>(OrderService, (c) => new OrderService(new StripeProcessor(), c.resolve(LoggerToken)));
console.assert(scoped.resolve(LoggerToken) === scoped.resolve(LoggerToken));       // singleton
console.assert(scoped.resolve(OrderService) !== scoped.resolve(OrderService));   // transient

// Testing is the point: inject a fake without touching OrderService.
const fake: PaymentProcessor = { charge: (amount) => amount < 50 };
console.assert(new OrderService(fake, new ConsoleLogger()).checkout(10.0));
console.assert(!new OrderService(fake, new ConsoleLogger()).checkout(99.0));
console.log("All DI examples ran.");
