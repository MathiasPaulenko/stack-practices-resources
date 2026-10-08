import java.util.*;

/**
 * Role Pattern — runnable example.
 *
 * Attach/detach roles on a Person entity at runtime and check
 * capabilities through role objects.
 *
 * Run: javac RolePattern.java && java RolePattern
 */
public class RolePattern {

    interface Role {
        String getRoleName();
        boolean canPerform(String action);
    }

    static class CustomerRole implements Role {
        private int loyaltyPoints = 0;

        public String getRoleName() { return "customer"; }
        public boolean canPerform(String action) {
            return List.of("browse", "purchase", "review").contains(action);
        }
        public void earnPoints(int amount) { loyaltyPoints += amount; }
    }

    static class EmployeeRole implements Role {
        private final String department;
        private final double salary;

        EmployeeRole(String department, double salary) {
            this.department = department; this.salary = salary;
        }

        public String getRoleName() { return "employee"; }
        public boolean canPerform(String action) {
            return List.of("browse", "inventory", "support", "refund").contains(action);
        }
        public String processRefund(String orderId) {
            return "Refund processed for " + orderId;
        }
    }

    static class Person {
        private final String personId;
        private final String name;
        private final Map<String, Role> roles = new HashMap<>();
        private final List<Map<String, String>> history = new ArrayList<>();

        Person(String personId, String name) {
            this.personId = personId; this.name = name;
        }

        public void assignRole(Role role) {
            roles.put(role.getRoleName(), role);
            history.add(Map.of("action", "assigned", "role", role.getRoleName()));
        }

        public void revokeRole(String roleName) {
            if (roles.remove(roleName) != null) {
                history.add(Map.of("action", "revoked", "role", roleName));
            }
        }

        public boolean hasRole(String roleName) { return roles.containsKey(roleName); }
        public Role getRole(String roleName) { return roles.get(roleName); }

        public boolean canPerform(String action) {
            return roles.values().stream().anyMatch(r -> r.canPerform(action));
        }

        public List<String> getRoles() { return new ArrayList<>(roles.keySet()); }
    }

    public static void main(String[] args) {
        Person person = new Person("P-001", "Alice");
        person.assignRole(new CustomerRole());
        person.assignRole(new EmployeeRole("Sales", 75000));

        System.out.println("Roles: " + person.getRoles());
        System.out.println("Can browse: " + person.canPerform("browse"));
        System.out.println("Can refund: " + person.canPerform("refund"));

        Role emp = person.getRole("employee");
        if (emp instanceof EmployeeRole e) {
            System.out.println(e.processRefund("ORD-123"));
        }

        person.revokeRole("customer");
        System.out.println("Roles after revoke: " + person.getRoles());
    }
}
