// Marker Interface Pattern — Java demo
// Compile: javac MarkerDemo.java && java MarkerDemo
// (All supporting classes are package-private; the public class drives the demo.)

// Custom marker interfaces — empty by design
interface Auditable {}
interface Immutable {}

class Transaction implements Auditable {
    private final String id;
    private final double amount;

    public Transaction(String id, double amount) {
        this.id = id; this.amount = amount;
    }

    public String getId() { return id; }
    public double getAmount() { return amount; }
}

class MutableConfig {
    private String value;
    public MutableConfig(String value) { this.value = value; }
    public String getValue() { return value; }
    public void setValue(String value) { this.value = value; }
}

class AuditFramework {
    public void logIfAuditable(Object obj) {
        if (obj instanceof Auditable) {
            System.out.println("AUDIT: " + obj.getClass().getSimpleName() + " was accessed");
        }
    }
}

class ValidationFramework {
    public void validateImmutable(Object obj) {
        if (obj instanceof Immutable) {
            System.out.println("VALIDATED: " + obj.getClass().getSimpleName() + " is immutable");
        }
    }
}

public class MarkerDemo {
    public static void main(String[] args) {
        Transaction tx = new Transaction("TX-001", 100.0);
        new AuditFramework().logIfAuditable(tx);                     // logs
        new AuditFramework().logIfAuditable(new MutableConfig("x")); // doesn't log
        new ValidationFramework().validateImmutable(tx);             // doesn't validate
    }
}
