# branch_by_abstraction.py — swap implementations behind a common interface
from abc import ABC, abstractmethod

class PaymentService(ABC):
    @abstractmethod
    def charge(self, customer_id: str, amount: float) -> dict:
        pass

class LegacyPaymentService(PaymentService):
    def charge(self, customer_id: str, amount: float) -> dict:
        # Legacy implementation
        return {"processor": "legacy", "status": "charged", "amount": amount}

class NewPaymentService(PaymentService):
    def charge(self, customer_id: str, amount: float) -> dict:
        # New implementation
        return {"processor": "stripe", "status": "charged", "amount": amount}

class PaymentServiceFactory:
    @staticmethod
    def create(use_new: bool = False) -> PaymentService:
        if use_new:
            return NewPaymentService()
        return LegacyPaymentService()

# Usage — switch by config flag
service = PaymentServiceFactory.create(use_new=True)
result = service.charge("cust_123", 99.99)
