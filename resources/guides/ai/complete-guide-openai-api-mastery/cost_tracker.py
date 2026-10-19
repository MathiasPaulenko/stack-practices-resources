"""Per-call cost accounting with a per-model breakdown."""
from openai import OpenAI

client = OpenAI()


class CostTracker:
    # Approximate USD per 1M tokens — check openai.com/pricing before relying on these.
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "text-embedding-3-small": {"input": 0.02, "output": 0.0},
    }

    def __init__(self):
        self.costs: list[dict] = []

    def track(self, model: str, input_tokens: int, output_tokens: int) -> None:
        if model not in self.PRICING:
            return
        pricing = self.PRICING[model]
        cost = (input_tokens / 1_000_000 * pricing["input"]) + (
            output_tokens / 1_000_000 * pricing["output"]
        )
        self.costs.append(
            {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
            }
        )

    def total_cost(self) -> float:
        return sum(c["cost"] for c in self.costs)

    def summary(self) -> dict:
        by_model: dict[str, dict] = {}
        for c in self.costs:
            slot = by_model.setdefault(c["model"], {"calls": 0, "cost": 0.0, "tokens": 0})
            slot["calls"] += 1
            slot["cost"] += c["cost"]
            slot["tokens"] += c["input_tokens"] + c["output_tokens"]
        return {
            "total_cost": self.total_cost(),
            "by_model": by_model,
            "total_calls": len(self.costs),
        }


if __name__ == "__main__":
    tracker = CostTracker()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hi in one word."}],
    )
    tracker.track(
        "gpt-4o-mini",
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
    )
    print(response.choices[0].message.content)
    print(tracker.summary())
