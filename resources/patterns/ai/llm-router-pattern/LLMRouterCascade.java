import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * LLM Router Pattern — runnable demo.
 *
 * Classifies queries by complexity (rules-based) and routes them to a tier
 * (small/medium/large). CascadeRouter adds quality-gated escalation.
 * Generate is mocked so the demo runs offline — swap {@code mockGenerate}
 * for real provider calls to use it for real.
 *
 * Run: javac LLMRouterCascade.java && java LLMRouterCascade
 */
public class LLMRouterCascade {

    record ModelConfig(String name, int maxTokens, double costPer1k, int latencyMs) {}

    record Response(String model, String content, int tokensUsed, double cost) {}

    record Classification(String level, double confidence) {}

    static final Map<String, ModelConfig> MODELS = Map.of(
        "small",  new ModelConfig("gpt-4o-mini",  4096, 0.0006, 200),
        "medium", new ModelConfig("gpt-4o",       8192, 0.005,  500),
        "large",  new ModelConfig("o1",          16384, 0.015,  2000)
    );

    static final Map<String, Integer> TIER_RANK = Map.of("small", 0, "medium", 1, "large", 2);
    static final Map<String, Integer> LEVEL_RANK = Map.of("low", 0, "medium", 1, "high", 2);
    static final List<String> TIERS = List.of("small", "medium", "large");

    static final List<Pattern> COMPLEX = List.of(
        Pattern.compile("analyze|design|architect|compare|evaluate"),
        Pattern.compile("debug|refactor|optimize|review"),
        Pattern.compile("step.by.step|detailed|thorough"),
        Pattern.compile("legal|medical|financial|security")
    );
    static final List<Pattern> SIMPLE = List.of(
        Pattern.compile("^\\s*(what|who|when|where|is|are|can|do)\\s"),
        Pattern.compile("calculate|convert|format|translate"),
        Pattern.compile("summarize|rewrite|paraphrase")
    );

    static Classification classifyComplexity(String text) {
        String lower = text.toLowerCase();
        int score = 0;
        for (Pattern p : COMPLEX) if (p.matcher(lower).find()) score += 2;
        for (Pattern p : SIMPLE) if (p.matcher(lower).find()) score -= 2;

        int words = text.split(" ").length;
        if (words > 100) score += 2;
        else if (words < 20) score -= 1;

        if (score >= 2)  return new Classification("high",   Math.min(0.5 + score * 0.15, 1.0));
        if (score <= -2) return new Classification("low",    Math.min(0.5 - score * 0.15, 1.0));
        return new Classification("medium", 0.5);
    }

    static String routeToModel(String complexity) {
        return switch (complexity) {
            case "low" -> "small";
            case "high" -> "large";
            default -> "medium";
        };
    }

    /** A tier under the query's true level answers thin. */
    static Response mockGenerate(String tier, ModelConfig model, String prompt) {
        int required = LEVEL_RANK.get(classifyComplexity(prompt).level());
        if (TIER_RANK.get(tier) < required) {
            return new Response(model.name(), "[" + model.name() + "] I can't fully answer that.", 12, 0.0);
        }
        int tokens = Math.min(Math.max(60, prompt.split(" ").length * 2), model.maxTokens());
        double cost = (tokens / 1000.0) * model.costPer1k();
        return new Response(model.name(), "[" + model.name() + "] Response to: "
            + prompt.substring(0, Math.min(50, prompt.length())) + "...", tokens, cost);
    }

    static class LLMRouter {
        int routed, escalated;
        double totalCost, baselineCost;

        void charge(Response r) {
            routed++;
            totalCost += r.cost();
            baselineCost += (r.tokensUsed() / 1000.0) * MODELS.get("large").costPer1k();
        }

        Response handle(String queryText) {
            Classification c = classifyComplexity(queryText);
            String key = routeToModel(c.level());
            System.out.printf("  [%s @ %.2f] -> %s%n", c.level(), c.confidence(), MODELS.get(key).name());
            Response r = mockGenerate(key, MODELS.get(key), queryText);
            charge(r);
            return r;
        }

        void report() {
            double savings = 1 - totalCost / Math.max(baselineCost, 1e-9);
            System.out.printf("  %d calls | %d escalations | cost $%.6f vs always-large $%.6f | saved %.0f%%%n",
                routed, escalated, totalCost, baselineCost, savings * 100);
        }
    }

    /** Start cheap, verify the response, escalate one tier on failure. */
    static class CascadeRouter extends LLMRouter {
        boolean qualityOk(Response r) {
            return r.tokensUsed() >= 30 && !r.content().contains("I can't");
        }

        @Override
        Response handle(String queryText) {
            Classification c = classifyComplexity(queryText);
            int start = TIERS.indexOf(routeToModel(c.level()));
            if (c.confidence() < 0.7) start = Math.max(start - 1, 0); // unsure: start lower, verify

            for (int i = start; i < TIERS.size(); i++) {
                String tier = TIERS.get(i);
                Response r = mockGenerate(tier, MODELS.get(tier), queryText);
                charge(r);
                if (qualityOk(r) || tier.equals("large")) {
                    System.out.printf("  [%s @ %.2f] -> %s%n", c.level(), c.confidence(), MODELS.get(tier).name());
                    return r;
                }
                escalated++;
                System.out.printf("  [%s @ %.2f] %s thin -> escalate%n",
                    c.level(), c.confidence(), MODELS.get(tier).name());
            }
            return null;
        }
    }

    public static void main(String[] args) {
        List<String> queries = List.of(
            "What is the capital of France?",
            "Analyze this contract for liability clauses and suggest revisions",
            "Convert 100 degrees Celsius to Fahrenheit",
            "Design a microservices architecture for an e-commerce platform with 10M users",
            "Translate 'good morning' to Spanish",
            "Should I refactor this function or leave it as is?"  // borderline -> medium
        );

        System.out.println("== One-shot router ==");
        LLMRouter router = new LLMRouter();
        for (String q : queries) router.handle(q);
        router.report();

        System.out.println("\n== Cascade router (verify + escalate) ==");
        CascadeRouter cascade = new CascadeRouter();
        for (String q : queries) cascade.handle(q);
        cascade.report();
    }
}
