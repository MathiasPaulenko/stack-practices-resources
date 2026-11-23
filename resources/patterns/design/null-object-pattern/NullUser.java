import java.util.List;

/**
 * Null Object pattern in Java: User interface with real and null implementations.
 * Compile: javac NullUser.java && java NullUser.Demo
 */
interface User {
    String getName();
    boolean hasAccess(String resource);
    List<String> getPermissions();
}

class RealUser implements User {
    private final String name;
    private final List<String> permissions;

    public RealUser(String name, List<String> permissions) {
        this.name = name;
        this.permissions = permissions;
    }

    public String getName() { return name; }
    public boolean hasAccess(String resource) {
        return permissions.contains(resource);
    }
    public List<String> getPermissions() { return permissions; }
}

public class NullUser implements User {
    public String getName() { return "Guest"; }
    public boolean hasAccess(String resource) { return false; }
    public List<String> getPermissions() { return List.of(); }

    public static class Demo {
        public static User findUser(int id) {
            if (id == 1) return new RealUser("Alice", List.of("reports", "settings"));
            return new NullUser(); // Always returns a valid User
        }

        public static void main(String[] args) {
            User user = findUser(999);
            System.out.println(user.getName());            // Guest
            System.out.println(user.hasAccess("admin"));   // false
            System.out.println(user.getPermissions());     // []
        }
    }
}
