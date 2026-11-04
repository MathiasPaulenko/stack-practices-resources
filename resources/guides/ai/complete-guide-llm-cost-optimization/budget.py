"""Budget guard: soft alert at threshold, hard stop at budget."""
from datetime import date

PRICING = {"gpt-4o": (2.50, 10.00), "gpt-4o-mini": (0.15, 0.60)}


class BudgetController:
    def __init__(self, daily_budget: float = 10.0, alert_at: float = 0.8):
        self.daily_budget, self.alert_at, self.spent = daily_budget, alert_at, {}

    def check(self, estimated_cost: float) -> str:
        projected = self.spent.get(date.today().isoformat(), 0) + estimated_cost
        if projected > self.daily_budget:
            return "stop"
        if projected > self.daily_budget * self.alert_at:
            return "alert"
        return "ok"

    def record(self, model: str, input_tokens: int, output_tokens: int):
        p = PRICING.get(model, (0, 0))
        cost = input_tokens / 1e6 * p[0] + output_tokens / 1e6 * p[1]
        today = date.today().isoformat()
        self.spent[today] = self.spent.get(today, 0) + cost
