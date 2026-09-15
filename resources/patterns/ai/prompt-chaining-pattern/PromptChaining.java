import java.util.*;
import java.util.function.Predicate;

/**
 * Prompt Chaining Pattern - Java implementation.
 *
 * Chain multiple LLM calls where each step's output feeds the next step's input.
 * Break complex tasks into smaller, verifiable prompts for better results.
 */
public class PromptChaining {

    record ChainStep(String name, String promptTemplate, String model,
                     double temperature, int maxRetries, Predicate<String> validator) {}

    record ChainResult(String stepName, String input, String output, boolean success, int retries) {}

    /** Simulate an LLM API call. Replace with your actual LLM client. */
    static String mockLlmCall(String prompt, String model, double temperature) {
        return "[" + model + "] Processed: " + prompt.substring(0, Math.min(60, prompt.length())) + "...";
    }

    static List<ChainResult> runChain(List<ChainStep> steps, String initialInput) {
        List<ChainResult> results = new ArrayList<>();
        String currentInput = initialInput;

        for (ChainStep step : steps) {
            String prompt = step.promptTemplate().replace("{input}", currentInput);
            boolean success = false;
            String output = "";
            int retries = 0;

            for (int attempt = 0; attempt <= step.maxRetries(); attempt++) {
                output = mockLlmCall(prompt, step.model(), step.temperature());
                retries = attempt;

                if (step.validator() != null && !step.validator().test(output)) {
                    System.out.printf("  Step '%s' validation failed (attempt %d)%n", step.name(), attempt + 1);
                    continue;
                }

                success = true;
                break;
            }

            results.add(new ChainResult(step.name(), currentInput, output, success, retries));

            if (!success) {
                System.out.printf("Chain stopped at '%s' after %d attempts%n", step.name(), retries + 1);
                break;
            }

            currentInput = output;
            System.out.printf("Step '%s' completed%n", step.name());
        }

        return results;
    }

    public static void main(String[] args) {
        Predicate<String> nonEmpty = s -> s.trim().length() > 10;
        Predicate<String> hasCode = s -> s.contains("```") || s.contains("void ") || s.contains("public ");

        var steps = List.of(
            new ChainStep("extract_requirements",
                "Extract key requirements from:\n{input}\n\nList as bullet points.",
                "gpt-4o", 0.2, 2, nonEmpty),
            new ChainStep("generate_code",
                "Generate code from these requirements:\n{input}\n\nProvide working code.",
                "gpt-4o", 0.3, 2, hasCode),
            new ChainStep("review_code",
                "Review this code for bugs:\n{input}\n\nList issues found.",
                "gpt-4o", 0.5, 2, nonEmpty),
            new ChainStep("format_report",
                "Create a summary report:\n{input}\n\nFormat as markdown.",
                "gpt-4o-mini", 0.7, 2, null)
        );

        var results = runChain(steps,
            "Build a REST API endpoint that accepts JSON, validates input, and returns 201 on success");

        System.out.printf("%nChain completed: %d/%d steps%n", results.size(), steps.size());
        for (ChainResult r : results) {
            String status = r.success() ? "OK" : "FAILED";
            System.out.printf("  %s: %s (retries: %d)%n", r.stepName(), status, r.retries());
        }
    }
}
