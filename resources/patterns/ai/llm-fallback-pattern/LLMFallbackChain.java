import java.util.List;
import java.util.Set;

/**
 * LLM Fallback Pattern — runnable demo (Java 17+).
 *
 * Provider chain with per-provider retry budgets and a retryable /
 * non-retryable error taxonomy. Mock provider call — no API keys needed.
 *
 * Run: javac LLMFallbackChain.java && java LLMFallbackChain
 */
public class LLMFallbackChain {

    enum ErrorType { RATE_LIMIT, TIMEOUT, SERVER_ERROR, AUTH, INVALID_REQUEST, UNKNOWN }

    static final Set<ErrorType> RETRYABLE =
        Set.of(ErrorType.RATE_LIMIT, ErrorType.TIMEOUT, ErrorType.SERVER_ERROR);

    static class LLMException extends Exception {
        final ErrorType type;
        final String provider;
        LLMException(ErrorType type, String message, String provider) {
            super(message);
            this.type = type;
            this.provider = provider;
        }
    }

    record ProviderConfig(String name, String model, int maxRetries,
                          double baseDelay, double maxDelay) {}

    record LLMResponse(String provider, String model, String content,
                       double latencyMs, boolean fromFallback) {}

    interface ProviderCall {
        String call(String provider, String model, String prompt) throws LLMException;
    }

    private final List<ProviderConfig> providers;
    private final ProviderCall call;
    private final String staticFallback;

    public LLMFallbackChain(List<ProviderConfig> providers, ProviderCall call,
                            String staticFallback) {
        this.providers = providers;
        this.call = call;
        this.staticFallback = staticFallback;
    }

    private static double exponentialBackoff(int attempt, double base, double maxDelay) {
        double delay = Math.min(base * Math.pow(2, attempt), maxDelay);
        return delay + Math.random() * 0.1 * delay; // jitter
    }

    private String callWithRetry(ProviderConfig p, String prompt) throws LLMException {
        for (int attempt = 0; attempt <= p.maxRetries(); attempt++) {
            try {
                return call.call(p.name(), p.model(), prompt);
            } catch (LLMException e) {
                if (!RETRYABLE.contains(e.type)) throw e;
                if (attempt >= p.maxRetries()) throw e;
                double delay = exponentialBackoff(attempt, p.baseDelay(), p.maxDelay());
                System.out.printf("  [%s] %s, retrying in %.1fs...%n", p.name(), e.type, delay);
                try {
                    Thread.sleep((long) Math.min(delay * 1000, 500)); // capped for the demo
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw e;
                }
            }
        }
        throw new IllegalStateException("unreachable");
    }

    public LLMResponse complete(String prompt) {
        for (int i = 0; i < providers.size(); i++) {
            ProviderConfig p = providers.get(i);
            try {
                long start = System.nanoTime();
                String content = callWithRetry(p, prompt);
                double latency = (System.nanoTime() - start) / 1_000_000.0;
                return new LLMResponse(p.name(), p.model(), content, latency, i > 0);
            } catch (LLMException e) {
                // Log every fallthrough — a silent chain hides provider outages
                System.out.printf("  [%s] Failed: %s - %s%n", p.name(), e.type, e.getMessage());
            }
        }
        return new LLMResponse("static", "none", staticFallback, 0, true);
    }

    private static String mockProviderCall(String provider, String model, String prompt)
            throws LLMException {
        String p = prompt.toLowerCase();
        if (provider.equals("openai") && p.contains("rate limit"))
            throw new LLMException(ErrorType.RATE_LIMIT, "Rate limit exceeded", provider);
        if (provider.equals("anthropic") && p.contains("timeout"))
            throw new LLMException(ErrorType.TIMEOUT, "Request timed out", provider);
        if (provider.equals("local") && p.contains("auth"))
            throw new LLMException(ErrorType.AUTH, "Invalid API key", provider);
        return "[" + provider + "/" + model + "] Response to: " + prompt.substring(0, Math.min(40, prompt.length())) + "...";
    }

    public static void main(String[] args) {
        var chain = new LLMFallbackChain(
            List.of(
                new ProviderConfig("openai", "gpt-4o", 2, 1.0, 30.0),
                new ProviderConfig("anthropic", "claude-3.5-sonnet", 1, 2.0, 30.0),
                new ProviderConfig("local", "llama-3-70b", 1, 0.5, 30.0)
            ),
            LLMFallbackChain::mockProviderCall,
            "I'm unable to respond right now. Please try again later."
        );

        String[] testPrompts = {
            "What is machine learning?",
            "This prompt will trigger rate limit on OpenAI",
            "This prompt will trigger timeout on Anthropic too",
            "This prompt will trigger auth error on local provider"
        };

        for (String prompt : testPrompts) {
            System.out.println("\nPrompt: " + prompt);
            LLMResponse r = chain.complete(prompt);
            System.out.printf("  Provider: %s/%s%n", r.provider(), r.model());
            System.out.printf("  Fallback: %s%n", r.fromFallback());
        }
    }
}
