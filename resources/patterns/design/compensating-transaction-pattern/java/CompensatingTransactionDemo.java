import java.util.*;
import java.util.function.*;

// Compensating Transaction — runnable saga demo.
// Compile and run: javac CompensatingTransactionDemo.java && java CompensatingTransactionDemo
// Domain services live as package-private classes in this same file.

class PaymentService {
    private final Map<String, Map<String, Object>> charges = new HashMap<>();

    public boolean charge(String orderId, double amount) {
        Map<String, Object> charge = new HashMap<>();
        charge.put("amount", amount);
        charge.put("status", "charged");
        charges.put(orderId, charge);
        System.out.println("  [Payment] Charged $" + amount + " for " + orderId);
        return true;
    }

    public boolean refund(String orderId) {
        Map<String, Object> charge = charges.get(orderId);
        if (charge != null) {
            charge.put("status", "refunded");
            System.out.println("  [Payment] Refunded $" + charge.get("amount") + " for " + orderId);
            return true;
        }
        return false;
    }
}

class InventoryService {
    private final Map<String, Integer> stock = new HashMap<>(Map.of("SKU-001", 100));
    private final Map<String, Map<String, Object>> reservations = new HashMap<>();

    public boolean reserve(String orderId, String sku, int qty) {
        int available = stock.getOrDefault(sku, 0);
        if (available >= qty) {
            stock.put(sku, available - qty);
            Map<String, Object> res = new HashMap<>();
            res.put("sku", sku);
            res.put("qty", qty);
            reservations.put(orderId, res);
            System.out.println("  [Inventory] Reserved " + qty + "x " + sku);
            return true;
        }
        System.out.println("  [Inventory] Insufficient stock for " + sku);
        return false;
    }

    public boolean release(String orderId) {
        Map<String, Object> res = reservations.remove(orderId);
        if (res != null) {
            String sku = (String) res.get("sku");
            int qty = (Integer) res.get("qty");
            stock.put(sku, stock.get(sku) + qty);
            System.out.println("  [Inventory] Released " + qty + "x " + sku);
            return true;
        }
        return false;
    }
}

class SagaStep {
    final String name;
    final Supplier<Boolean> action;
    final Runnable compensate;

    SagaStep(String name, Supplier<Boolean> action, Runnable compensate) {
        this.name = name;
        this.action = action;
        this.compensate = compensate;
    }
}

class SagaOrchestrator {
    private final List<SagaStep> completedSteps = new ArrayList<>();

    public boolean execute(List<SagaStep> steps) {
        for (SagaStep step : steps) {
            System.out.println("Executing: " + step.name);
            if (step.action.get()) {
                completedSteps.add(step);
            } else {
                System.out.println(step.name + " failed! Compensating...");
                compensate();
                return false;
            }
        }
        return true;
    }

    private void compensate() {
        List<SagaStep> reverse = new ArrayList<>(completedSteps);
        Collections.reverse(reverse);
        for (SagaStep step : reverse) {
            System.out.println("Compensating: " + step.name);
            try {
                step.compensate.run();
            } catch (Exception e) {
                System.err.println("WARNING: Compensation failed for " + step.name + ": " + e.getMessage());
            }
        }
    }
}

public class CompensatingTransactionDemo {
    public static void main(String[] args) {
        PaymentService payments = new PaymentService();
        InventoryService inventory = new InventoryService();
        SagaOrchestrator saga = new SagaOrchestrator();

        // The reserve step fails (no SKU-999 in stock), triggering compensation.
        List<SagaStep> steps = List.of(
            new SagaStep("charge", () -> payments.charge("ORD-001", 99.99),
                    () -> payments.refund("ORD-001")),
            new SagaStep("reserve", () -> inventory.reserve("ORD-001", "SKU-999", 500),
                    () -> inventory.release("ORD-001"))
        );

        boolean success = saga.execute(steps);
        System.out.println("Saga result: " + (success ? "SUCCESS" : "FAILED (compensated)"));
    }
}
