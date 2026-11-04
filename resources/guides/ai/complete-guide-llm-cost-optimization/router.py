"""Model router + cascading fallback — cheapest model that can do the job."""
import re
from openai import OpenAI

client = OpenAI()

PRICING = {"gpt-4o": (2.50, 10.00), "gpt-4o-mini": (0.15, 0.60)}


class ModelRouter:
    def __init__(self):
        self.rules = [
            (r"^(summarize|classify|extract)", "gpt-4o-mini"),
            (r"^(write|create|generate|code|debug|analyze)", "gpt-4o"),
        ]
        self.default_model = "gpt-4o-mini"

    def select_model(self, prompt: str) -> str:
        low = prompt.lower().strip()
        for pattern, model in self.rules:
            if re.search(pattern, low):
                return model
        return "gpt-4o-mini" if len(prompt) // 4 < 100 else self.default_model

    def complete(self, prompt: str, **kwargs) -> dict:
        model = self.select_model(prompt)
        r = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], **kwargs)
        p = PRICING.get(model, (0, 0))
        cost = r.usage.prompt_tokens / 1e6 * p[0] + r.usage.completion_tokens / 1e6 * p[1]
        return {"content": r.choices[0].message.content, "model": model, "cost": cost}


class CascadingRouter:
    """Cheap first, escalate when the model signals uncertainty."""
    def __init__(self):
        self.client = OpenAI()

    def complete(self, prompt: str) -> dict:
        r = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer. If unsure, say 'UNCERTAIN'."},
                {"role": "user", "content": prompt}],
            temperature=0.0)
        answer = r.choices[0].message.content
        if "UNCERTAIN" not in answer:
            return {"answer": answer, "model": "gpt-4o-mini"}
        r = self.client.chat.completions.create(
            model="gpt-4o", messages=[{"role": "user", "content": prompt}], temperature=0.0)
        return {"answer": r.choices[0].message.content, "model": "gpt-4o"}
