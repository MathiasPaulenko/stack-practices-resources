"""Token counting with tiktoken — count before you send."""
import tiktoken


class TokenManager:
    def __init__(self, model: str = "gpt-4o"):
        self.encoder = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def count_messages(self, messages: list[dict]) -> int:
        total = 0
        for msg in messages:
            total += 4
            for k, v in msg.items():
                total += len(self.encoder.encode(str(v)))
                if k == "name":
                    total -= 1
        return total + 2
