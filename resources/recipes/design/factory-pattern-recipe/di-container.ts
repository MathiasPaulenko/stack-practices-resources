// Minimal DI container using factory providers (TypeScript)
interface Container {
  bind<T>(token: string, factory: () => T): void;
  resolve<T>(token: string): T;
}

class SimpleContainer implements Container {
  private bindings: Map<string, () => unknown> = new Map();
  private instances: Map<string, unknown> = new Map();

  bind<T>(token: string, factory: () => T): void {
    this.bindings.set(token, factory);
  }

  resolve<T>(token: string): T {
    if (this.instances.has(token)) return this.instances.get(token) as T;
    const factory = this.bindings.get(token);
    if (!factory) throw new Error(`No binding for ${token}`);
    const instance = factory() as T;
    this.instances.set(token, instance);
    return instance;
  }
}

// Domain stubs to show wiring
class ConsoleLogger { log(msg: string) { console.log(`[log] ${msg}`); } }
class PostgresConnection {
  constructor(public url: string | undefined) {}
}
class UserRepository {
  constructor(private db: PostgresConnection, private logger: ConsoleLogger) {}
  findAll() { this.logger.log('findAll users'); return []; }
}
class UserService {
  constructor(private repo: UserRepository) {}
  async createUser(input: { email: string; name: string }) {
    this.repo.findAll();
    console.log('Created', input.email);
  }
}

const container = new SimpleContainer();
container.bind('Logger', () => new ConsoleLogger());
container.bind('Database', () => new PostgresConnection(process.env.DATABASE_URL));
container.bind('UserRepository', () =>
  new UserRepository(container.resolve<PostgresConnection>('Database'), container.resolve<ConsoleLogger>('Logger')));
container.bind('UserService', () => new UserService(container.resolve<UserRepository>('UserRepository')));

const userService = container.resolve<UserService>('UserService');
await userService.createUser({ email: 'user@example.com', name: 'Alice' });
