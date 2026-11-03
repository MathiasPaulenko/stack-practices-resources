import pybreaker
import requests

class PaymentService:
    def __init__(self):
        self.breaker = pybreaker.CircuitBreaker(
            fail_max=5,
            reset_timeout=30,
            expected_exception=requests.RequestException
        )

    @pybreaker.circuit
    def charge(self, amount):
        response = requests.post(
            "https://payment-api.example.com/charge",
            json={"amount": amount}
        )
        response.raise_for_status()
        return response.json()

service = PaymentService()

try:
    result = service.charge(100)
except pybreaker.CircuitBreakerError:
    result = fallback_charge(100)
