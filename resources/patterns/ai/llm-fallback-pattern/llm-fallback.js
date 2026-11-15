/**
 * LLM Fallback Pattern — runnable demo (Node.js).
 *
 * Provider chain with per-provider retry budgets and a retryable /
 * non-retryable error taxonomy. Mock provider call — no API keys needed.
 *
 * Run: node llm-fallback.js
 */

class LLMError extends Error {
  constructor(errorType, message, provider) {
    super(message);
    this.errorType = errorType;
    this.provider = provider;
  }
}

const RETRYABLE_ERRORS = new Set(["rate_limit", "timeout", "server_error"]);

function exponentialBackoff(attempt, base, maxDelay) {
  const delay = Math.min(base * Math.pow(2, attempt), maxDelay);
  return delay + Math.random() * 0.1 * delay;
}

function mockProviderCall(provider, model, prompt) {
  if (provider === "openai" && prompt.toLowerCase().includes("rate limit"))
    throw new LLMError("rate_limit", "Rate limit exceeded", provider);
  if (provider === "anthropic" && prompt.toLowerCase().includes("timeout"))
    throw new LLMError("timeout", "Request timed out", provider);
  if (provider === "local" && prompt.toLowerCase().includes("auth"))
    throw new LLMError("auth", "Invalid API key", provider);
  return `[${provider}/${model}] Response to: ${prompt.slice(0, 40)}...`;
}

class LLMFallbackChain {
  constructor(providers, staticFallback = "I'm unable to respond right now.") {
    this.providers = providers; // [{name, model, maxRetries, baseDelay, maxDelay}]
    this.staticFallback = staticFallback;
  }

  async _callWithRetry(provider, prompt) {
    for (let attempt = 0; attempt <= provider.maxRetries; attempt++) {
      try {
        return mockProviderCall(provider.name, provider.model, prompt);
      } catch (e) {
        if (!(e instanceof LLMError) || !RETRYABLE_ERRORS.has(e.errorType)) throw e;
        if (attempt >= provider.maxRetries) throw e;
        const delay = exponentialBackoff(attempt, provider.baseDelay, provider.maxDelay);
        console.log(`  [${provider.name}] ${e.errorType}, retrying in ${delay.toFixed(1)}s...`);
        await new Promise((r) => setTimeout(r, Math.min(delay * 1000, 500)));
      }
    }
  }

  async complete(prompt) {
    for (let i = 0; i < this.providers.length; i++) {
      const provider = this.providers[i];
      try {
        const start = Date.now();
        const content = await this._callWithRetry(provider, prompt);
        return {
          provider: provider.name,
          model: provider.model,
          content,
          latencyMs: Date.now() - start,
          fromFallback: i > 0,
        };
      } catch (e) {
        console.log(`  [${provider.name}] Failed: ${e.errorType ?? e.message}`);
        continue;
      }
    }
    return {
      provider: "static",
      model: "none",
      content: this.staticFallback,
      latencyMs: 0,
      fromFallback: true,
    };
  }
}

async function demo() {
  const chain = new LLMFallbackChain([
    { name: "openai", model: "gpt-4o", maxRetries: 2, baseDelay: 1.0, maxDelay: 30 },
    { name: "anthropic", model: "claude-3.5-sonnet", maxRetries: 1, baseDelay: 2.0, maxDelay: 30 },
    { name: "local", model: "llama-3-70b", maxRetries: 1, baseDelay: 0.5, maxDelay: 30 },
  ]);

  const testPrompts = [
    "What is machine learning?",
    "This prompt will trigger rate limit on OpenAI",
    "This prompt will trigger timeout on Anthropic too",
    "This prompt will trigger auth error on local provider",
  ];

  for (const prompt of testPrompts) {
    console.log(`\nPrompt: ${prompt}`);
    const response = await chain.complete(prompt);
    console.log(`  Provider: ${response.provider}/${response.model}`);
    console.log(`  Fallback: ${response.fromFallback}`);
  }
}

demo();
