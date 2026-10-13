import java.util.*;
import java.util.function.Consumer;

/**
 * Orchestrated saga: travel booking with compensating transactions.
 * The chargePayment step always fails so you can watch the rollback path.
 * Run: javac SagaOrchestrator.java && java SagaOrchestrator
 */
class SagaStep {
    String name;
    Consumer<Map<String, Object>> action;
    Consumer<Map<String, Object>> compensation;

    SagaStep(String name, Consumer<Map<String, Object>> action, Consumer<Map<String, Object>> compensation) {
        this.name = name;
        this.action = action;
        this.compensation = compensation;
    }
}

class SagaResult {
    boolean success;
    String error;
    int stepIndex;

    SagaResult(boolean success, String error, int stepIndex) {
        this.success = success;
        this.error = error;
        this.stepIndex = stepIndex;
    }
}

public class SagaOrchestrator {
    private final List<SagaStep> steps = new ArrayList<>();
    private final List<Map<String, Object>> completed = new ArrayList<>();

    void addStep(String name, Consumer<Map<String, Object>> action, Consumer<Map<String, Object>> compensation) {
        steps.add(new SagaStep(name, action, compensation));
    }

    SagaResult execute(Map<String, Object> context) {
        completed.clear();
        for (int i = 0; i < steps.size(); i++) {
            try {
                steps.get(i).action.accept(context);
                completed.add(new HashMap<>(context));
                System.out.println("Step '" + steps.get(i).name + "' completed");
            } catch (Exception e) {
                System.out.println("Step '" + steps.get(i).name + "' failed: " + e.getMessage());
                rollback(i);
                return new SagaResult(false, e.getMessage(), i);
            }
        }
        return new SagaResult(true, null, steps.size());
    }

    void rollback(int failedIndex) {
        System.out.println("Rolling back " + failedIndex + " completed steps...");
        for (int j = failedIndex - 1; j >= 0; j--) {
            SagaStep step = steps.get(j);
            if (step.compensation != null) {
                try {
                    step.compensation.accept(completed.get(j));
                    System.out.println("Compensated '" + step.name + "'");
                } catch (Exception e) {
                    System.out.println("Compensation failed: " + e.getMessage());
                }
            }
        }
    }

    public static void main(String[] args) {
        SagaOrchestrator saga = new SagaOrchestrator();
        saga.addStep("reserveFlight",
            ctx -> ctx.put("flight", "FL123"),
            ctx -> System.out.println("Canceling flight")
        );
        saga.addStep("reserveHotel",
            ctx -> ctx.put("hotel", "HT456"),
            ctx -> System.out.println("Canceling hotel")
        );
        saga.addStep("chargePayment",
            ctx -> { throw new RuntimeException("Payment declined"); },
            ctx -> System.out.println("Refunding payment")
        );

        SagaResult result = saga.execute(new HashMap<>(Map.of("user", "alice")));
        System.out.println("Success: " + result.success);
    }
}
