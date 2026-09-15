/**
 * Prompt Chaining Pattern - JavaScript implementation.
 *
 * Chain multiple LLM calls where each step's output feeds the next step's input.
 * Break complex tasks into smaller, verifiable prompts for better results.
 */

class ChainStep {
  constructor(name, promptTemplate, options = {}) {
    this.name = name;
    this.promptTemplate = promptTemplate;
    this.model = options.model || "gpt-4o";
    this.temperature = options.temperature ?? 0.7;
    this.maxRetries = options.maxRetries ?? 2;
    this.validator = options.validator || null;
  }
}

/**
 * Simulate an LLM API call. Replace with your actual LLM client.
 */
function mockLlmCall(prompt, model, temperature) {
  return `[${model}] Processed: ${prompt.slice(0, 60)}...`;
}

class PromptChain {
  constructor(steps) {
    this.steps = steps;
  }

  async run(initialInput) {
    const results = [];
    let currentInput = initialInput;

    for (const step of this.steps) {
      const prompt = step.promptTemplate.replace("{input}", currentInput);
      let success = false;
      let output = "";
      let retries = 0;

      for (let attempt = 0; attempt <= step.maxRetries; attempt++) {
        output = mockLlmCall(prompt, step.model, step.temperature);
        retries = attempt;

        if (step.validator && !step.validator(output)) {
          console.log(`  Step '${step.name}' validation failed (attempt ${attempt + 1})`);
          continue;
        }

        success = true;
        break;
      }

      results.push({ stepName: step.name, input: currentInput, output, success, retries });

      if (!success) {
        console.log(`Chain stopped at step '${step.name}' after ${retries + 1} attempts`);
        break;
      }

      currentInput = output;
      console.log(`Step '${step.name}' completed`);
    }

    return results;
  }
}

// --- Validators ---

function validateNonEmpty(text) {
  return text.trim().length > 10;
}

function validateHasCode(text) {
  return text.includes("```") || text.includes("function ") || text.includes("const ");
}

// --- Usage example ---

const chain = new PromptChain([
  new ChainStep("extract_requirements", "Extract key requirements from:\n{input}\n\nList as bullet points.", { temperature: 0.2, validator: validateNonEmpty }),
  new ChainStep("generate_code", "Generate code from these requirements:\n{input}\n\nProvide working code.", { temperature: 0.3, validator: validateHasCode }),
  new ChainStep("review_code", "Review this code for bugs:\n{input}\n\nList issues found.", { temperature: 0.5, validator: validateNonEmpty }),
  new ChainStep("format_report", "Create a summary report:\n{input}\n\nFormat as markdown.", { model: "gpt-4o-mini", temperature: 0.7 }),
]);

chain.run("Build a REST API endpoint that accepts JSON, validates input, and returns 201 on success").then(results => {
  console.log(`\nChain completed: ${results.length}/${chain.steps.length} steps`);
  results.forEach(r => {
    const status = r.success ? "OK" : "FAILED";
    console.log(`  ${r.stepName}: ${status} (retries: ${r.retries})`);
  });
});
