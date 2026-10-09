import java.util.*;

/**
 * Identity Map pattern — runnable single-file Java example.
 *
 * Source: https://stackpractices.com/patterns/identity-map-pattern/
 *
 * Run: javac IdentityMapDemo.java && java IdentityMapDemo
 * Expected output: true / true (same instance returned, collection queries reuse the map)
 *
 * The article version of UserMapper talks JDBC (java.sql). This file swaps the
 * database for an in-memory table so it compiles and runs with plain javac —
 * the IdentityMap part is identical either way.
 */
public class IdentityMapDemo {

    public static class User {
        private final int id;
        private String name;
        private String email;

        public User(int id, String name, String email) {
            this.id = id;
            this.name = name;
            this.email = email;
        }

        public int getId() { return id; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }

        @Override
        public String toString() {
            return "User(id=" + id + ", name='" + name + "')";
        }
    }

    static class IdentityMap {
        private final Map<Class<?>, Map<Object, Object>> map = new HashMap<>();

        @SuppressWarnings("unchecked")
        <T> T get(Class<T> type, Object key) {
            return (T) map.getOrDefault(type, Collections.emptyMap()).get(key);
        }

        <T> void add(Class<T> type, Object key, T entity) {
            map.computeIfAbsent(type, k -> new HashMap<>()).put(key, entity);
        }

        <T> boolean has(Class<T> type, Object key) {
            return map.getOrDefault(type, Collections.emptyMap()).containsKey(key);
        }
    }

    /** In-memory stand-in for a database table: id -> row */
    static class FakeUsersTable {
        private final Map<Integer, String[]> rows = new HashMap<>();

        FakeUsersTable() {
            rows.put(1, new String[] {"Alice", "alice@example.com"});
        }

        Optional<String[]> findRow(int id) {
            return Optional.ofNullable(rows.get(id));
        }

        Set<Integer> allIds() {
            return rows.keySet();
        }
    }

    static class UserMapper {
        private final FakeUsersTable table;
        private final IdentityMap identityMap;

        UserMapper(FakeUsersTable table, IdentityMap identityMap) {
            this.table = table;
            this.identityMap = identityMap;
        }

        User findById(int id) {
            User cached = identityMap.get(User.class, id);
            if (cached != null) return cached;

            return table.findRow(id)
                    .map(row -> {
                        User user = new User(id, row[0], row[1]);
                        identityMap.add(User.class, id, user);
                        return user;
                    })
                    .orElse(null);
        }

        List<User> findAll() {
            List<User> users = new ArrayList<>();
            for (int id : table.allIds()) {
                users.add(findById(id)); // collection queries reuse the map
            }
            return users;
        }
    }

    public static void main(String[] args) {
        FakeUsersTable table = new FakeUsersTable();
        IdentityMap im = new IdentityMap();
        UserMapper mapper = new UserMapper(table, im);

        User user1 = mapper.findById(1);
        User user2 = mapper.findById(1);
        System.out.println(user1 == user2); // true — same object instance

        List<User> all = mapper.findAll();
        System.out.println(all.get(0) == user1); // true — findAll reuses the map
    }
}
