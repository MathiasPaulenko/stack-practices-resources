// Lightweight DI container — companion to
// https://stackpractices.com/recipes/dependency-injection/
// ~60 lines, no dependencies. Adapt freely.

type Factory<T> = () => T;

export class DIContainer {
  private factories: Map<string, Factory<any>> = new Map();
  private singletons: Map<string, any> = new Map();
  private scoped: Map<string, any> = new Map();

  registerTransient<T>(key: string, factory: Factory<T>): void {
    this.factories.set(key, factory);
  }

  registerSingleton<T>(key: string, factory: Factory<T>): void {
    this.factories.set(key, () => {
      if (!this.singletons.has(key)) {
        this.singletons.set(key, factory());
      }
      return this.singletons.get(key);
    });
  }

  registerScoped<T>(key: string, factory: Factory<T>): void {
    this.factories.set(key, () => {
      if (!this.scoped.has(key)) {
        this.scoped.set(key, factory());
      }
      return this.scoped.get(key);
    });
  }

  resolve<T>(key: string): T {
    const factory = this.factories.get(key);
    if (!factory) {
      throw new Error(`No service registered for key: ${key}`);
    }
    return factory();
  }

  /** Validate the whole graph at startup — resolves every key once. */
  validate(): void {
    for (const key of this.factories.keys()) {
      this.resolve(key);
    }
  }

  beginScope(): void {
    this.scoped.clear();
  }

  endScope(): void {
    this.scoped.clear();
  }
}

// --- Example wiring (composition root) ---
//
// const container = new DIContainer();
// container.registerSingleton('db', () => new PostgresPool({ url: process.env.DB_URL }));
// container.registerSingleton('emailService', () => new SendGridEmailService(process.env.KEY));
// container.registerScoped('userRepository', () => new PostgresUserRepository(container.resolve('db')));
// container.registerScoped('userService', () =>
//   new UserService(container.resolve('emailService'), container.resolve('userRepository'))
// );
// container.validate();
//
// // Per request:
// container.beginScope();
// const svc = container.resolve<UserService>('userService');
// // ... handle request ...
// container.endScope();
