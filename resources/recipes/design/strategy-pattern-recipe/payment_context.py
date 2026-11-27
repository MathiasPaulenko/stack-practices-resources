from typing import Protocol

class PaymentStrategy(Protocol):
    def pay(self, amount: float) -> str: ...

class CreditCardStrategy:
    def __init__(self, card_number: str, cvv: str):
        self._card = card_number
        self._cvv = cvv

    def pay(self, amount: float) -> str:
        return f"Charged ${amount:.2f} to card ending in {self._card[-4:]}"

class PayPalStrategy:
    def __init__(self, email: str):
        self._email = email

    def pay(self, amount: float) -> str:
        return f"Charged ${amount:.2f} via PayPal ({self._email})"

class CryptoStrategy:
    def __init__(self, wallet: str):
        self._wallet = wallet

    def pay(self, amount: float) -> str:
        return f"Charged {amount / 50000:.8f} BTC from {self._wallet[:8]}..."

class PaymentContext:
    def __init__(self):
        self._strategies: dict[str, PaymentStrategy] = {}

    def register(self, key: str, strategy: PaymentStrategy):
        self._strategies[key] = strategy

    def pay(self, method: str, amount: float) -> str:
        strategy = self._strategies.get(method)
        if strategy is None:
            raise ValueError(f"Unknown payment method: {method}")
        return strategy.pay(amount)

# Usage — register strategies, select by method key
context = PaymentContext()
context.register('credit-card', CreditCardStrategy('4111111111111234', '123'))
context.register('paypal', PayPalStrategy('user@example.com'))
context.register('crypto', CryptoStrategy('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'))

result = context.pay('paypal', 99.99)
