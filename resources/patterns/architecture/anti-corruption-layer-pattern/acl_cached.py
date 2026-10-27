# acl_cached.py — ACL with caching to reduce legacy calls
from functools import lru_cache
from acl.customer_acl import CustomerACL, Customer

class CachedCustomerACL:
    """Wraps the ACL with caching to reduce legacy system load."""

    def __init__(self, inner_acl: CustomerACL):
        self._inner = inner_acl

    @lru_cache(maxsize=1000)
    def get_customer(self, customer_id: str) -> Customer:
        return self._inner.get_customer(customer_id)

    def create_customer(self, customer: Customer) -> Customer:
        result = self._inner.create_customer(customer)
        # Cache the new customer
        self.get_customer.cache_clear()
        return result

    def update_customer(self, customer: Customer) -> Customer:
        result = self._inner.update_customer(customer)
        # Invalidate cache for this customer
        self.get_customer.cache_clear()
        return result

    def suspend_customer(self, customer_id: str) -> Customer:
        result = self._inner.suspend_customer(customer_id)
        self.get_customer.cache_clear()
        return result
