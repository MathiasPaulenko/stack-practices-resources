# domain/customer_service.py — new domain service uses ACL, not legacy
from acl.customer_acl import CustomerACL, Customer, CustomerStatus

class CustomerService:
    """New domain service — knows nothing about the legacy system."""

    def __init__(self, acl: CustomerACL):
        self._acl = acl

    def onboard_customer(self, email: str, full_name: str) -> Customer:
        customer = Customer(
            id="",  # ACL will assign
            email=email,
            full_name=full_name,
            status=CustomerStatus.active(),
            created_at=""
        )
        return self._acl.create_customer(customer)

    def suspend(self, customer_id: str) -> Customer:
        return self._acl.suspend_customer(customer_id)

    def get_profile(self, customer_id: str) -> dict:
        customer = self._acl.get_customer(customer_id)
        if customer is None:
            raise ValueError(f"Customer {customer_id} not found")
        return {
            "id": customer.id,
            "email": customer.email,
            "name": customer.full_name,
            "status": customer.status.value
        }
