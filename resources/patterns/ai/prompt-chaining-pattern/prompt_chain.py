"""Prompt Chaining Pattern - Python implementation.

Chain multiple LLM calls where each step's output feeds the next step's input.
Break complex tasks into smaller, verifiable prompts for better results.
"""

from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class ChainStep:
    name: str
    prompt_template: str
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_retries: int = 2
    validator: Optional[Callable[[str], bool]] = None


@dataclass
class ChainResult:
    step_name: str
    input: str
    output: str
    success: bool
    retries: int


def mock_llm_call(prompt: str, model: str, temperature: float) -> str:
    """Simulate an LLM API call. Replace with your actual LLM client."""
    return f"[{model}] Processed: {prompt[:60]}..."


class PromptChain:
    def __init__(self, steps: List[ChainStep]):
        self.steps = steps

    def run(self, initial_input: str) -> List[ChainResult]:
        results: List[ChainResult] = []
        current_input = initial_input

        for step in self.steps:
            prompt = step.prompt_template.format(input=current_input)
            success = False
            output = ""
            retries = 0

            for attempt in range(step.max_retries + 1):
                output = mock_llm_call(prompt, step.model, step.temperature)
                retries = attempt

                if step.validator and not step.validator(output):
                    print(f"  Step '{step.name}' validation failed (attempt {attempt + 1})")
                    continue

                success = True
                break

            results.append(ChainResult(
                step_name=step.name,
                input=current_input,
                output=output,
                success=success,
                retries=retries,
            ))

            if not success:
                print(f"Chain stopped at step '{step.name}' after {retries + 1} attempts")
                break

            current_input = output
            print(f"Step '{step.name}' completed")

        return results


# --- Validators ---

def validate_non_empty(text: str) -> bool:
    return len(text.strip()) > 10


def validate_has_code(text: str) -> bool:
    return "```" in text or "def " in text or "function " in text


# --- Usage example ---

if __name__ == "__main__":
    chain = PromptChain([
        ChainStep(
            name="extract_requirements",
            prompt_template="Extract key requirements from this text:\n{input}\n\nList each requirement as a bullet point.",
            model="gpt-4o",
            temperature=0.2,
            validator=validate_non_empty,
        ),
        ChainStep(
            name="generate_code",
            prompt_template="Based on these requirements, generate code:\n{input}\n\nProvide working code with comments.",
            model="gpt-4o",
            temperature=0.3,
            validator=validate_has_code,
        ),
        ChainStep(
            name="review_code",
            prompt_template="Review this code for bugs and improvements:\n{input}\n\nList issues found.",
            model="gpt-4o",
            temperature=0.5,
            validator=validate_non_empty,
        ),
        ChainStep(
            name="format_report",
            prompt_template="Create a summary report from this review:\n{input}\n\nFormat as markdown with sections.",
            model="gpt-4o-mini",
            temperature=0.7,
        ),
    ])

    results = chain.run("Build a REST API endpoint that accepts JSON, validates input, and returns 201 on success")

    print(f"\nChain completed: {len(results)}/{len(chain.steps)} steps")
    for r in results:
        status = "OK" if r.success else "FAILED"
        print(f"  {r.step_name}: {status} (retries: {r.retries})")
