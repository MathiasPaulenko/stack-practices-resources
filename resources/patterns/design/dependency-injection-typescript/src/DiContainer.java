// DI container with explicit lifetimes — Java port of the article's
// TypeScript container. Factories wire the graph; lifetimes decide caching.

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

public class DiContainer {

    enum Lifetime { SINGLETON, TRANSIENT }

    @FunctionalInterface
    interface Factory<T> extends Function<Container, T> { }

    static class Container {
        private final Map<String, Factory<?>> registrations = new HashMap<>();
        private final Map<String, Lifetime> lifetimes = new HashMap<>();
        private final Map<String, Object> singletons = new HashMap<>();

        <T> Container register(String token, Factory<T> factory, Lifetime lifetime) {
            registrations.put(token, factory);
            lifetimes.put(token, lifetime);
            return this;
        }

        @SuppressWarnings("unchecked")
        <T> T resolve(String token) {
            Factory<T> factory = (Factory<T>) registrations.get(token);
            if (factory == null) throw new IllegalStateException("Nothing registered for " + token);

            if (lifetimes.get(token) == Lifetime.SINGLETON) {
                return (T) singletons.computeIfAbsent(token, t -> factory.apply(this));
            }
            return factory.apply(this);
        }

        ScopedContainer createScope() {
            return new ScopedContainer(this);
        }
    }

    static class ScopedContainer {
        private final Container root;
        private final Map<String, Object> cache = new HashMap<>();

        ScopedContainer(Container root) { this.root = root; }

        <T> T resolve(String token) {
            return (T) cache.computeIfAbsent(token, root::resolve);
        }
    }

    // --- services ---
    static class Database {
        List<Map<String, Object>> query(String sql) {
            return List.of(Map.of("id", 1, "name", "Alice"));
        }
    }

    static class Logger {
        void info(String msg) { System.out.println("[info] " + msg); }
    }

    static class UserRepository {
        private final Database db;
        private final Logger logger;
        UserRepository(Database db, Logger logger) { this.db = db; this.logger = logger; }
        List<Map<String, Object>> findAll() {
            logger.info("fetching users");
            return db.query("SELECT * FROM users");
        }
    }

    static class UserService {
        private final UserRepository repo;
        UserService(UserRepository repo) { this.repo = repo; }
        List<Map<String, Object>> getUsers() { return repo.findAll(); }
    }

    public static void main(String[] args) {
        Container container = new Container();
        container.register("db", c -> new Database(), Lifetime.SINGLETON);
        container.register("logger", c -> new Logger(), Lifetime.SINGLETON);
        container.register("repo", c -> new UserRepository(c.resolve("db"), c.resolve("logger")), Lifetime.TRANSIENT);
        container.register("users", c -> new UserService(c.resolve("repo")), Lifetime.TRANSIENT);

        UserService service = container.resolve("users");
        System.out.println("users: " + service.getUsers());
        System.out.println("singleton shared: " + (container.resolve("db") == container.resolve("db")));
        System.out.println("transient fresh: " + (container.resolve("repo") != container.resolve("repo")));

        ScopedContainer scopeA = container.createScope();
        ScopedContainer scopeB = container.createScope();
        System.out.println("scoped same in scope: " + (scopeA.resolve("repo") == scopeA.resolve("repo")));
        System.out.println("scoped differs across scopes: " + (scopeA.resolve("repo") != scopeB.resolve("repo")));
        System.out.println("singleton shared across scopes: " + (scopeA.resolve("db") == scopeB.resolve("db")));
    }
}
