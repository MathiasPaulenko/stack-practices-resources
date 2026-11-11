"""Simple Factory — payment provider chosen from a string parameter (Python).

Runnable: set STRIPE_API_KEY / PAYPAL_CLIENT_ID / PAYPAL_SECRET in the
environment, or accept the dev fallbacks used below.
"""
import os
from typing import Protocol


class PaymentProcessor(Protocol):
    def charge(self, amount: float, currency: str) -> dict: ...


class StripeProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def charge(self, amount: float, currency: str) -> dict:
        return {"provider": "stripe", "status": "success", "amount": amount}


class PayPalProcessor:
    def __init__(self, client_id: str, secret: str):
        self.client_id = client_id
        self.secret = secret

    def charge(self, amount: float, currency: str) -> dict:
        return {"provider": "paypal", "status": "success", "amount": amount}


class PaymentProcessorFactory:
    def create(self, provider: str) -> PaymentProcessor:
        if provider == "stripe":
            return StripeProcessor(api_key=os.environ.get("STRIPE_API_KEY", "sk_test_dev"))
        if provider == "paypal":
            return PayPalProcessor(
                client_id=os.environ.get("PAYPAL_CLIENT_ID", "dev-id"),
                secret=os.environ.get("PAYPAL_SECRET", "dev-secret"),
            )
        raise ValueError(f"Unknown provider: {provider}")


if __name__ == "__main__":
    factory = PaymentProcessorFactory()
    for provider in ("stripe", "paypal"):
        processor = factory.create(provider)
        print(processor.charge(99.99, "USD"))
