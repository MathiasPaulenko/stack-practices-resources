# acl/customer_acl.py — Anti-corruption layer for customer domain
from dataclasses import dataclass
from typing import Optional
from legacy.client import LegacyCustomerClient

# New domain model — clean, uses domain language
@dataclass(frozen=True)
class Customer:
    id: str
    email: str
    full_name: str
    status: CustomerStatus
    created_at: str

@dataclass(frozen=True)
class CustomerStatus:
    value: str  # "active", "suspended", "churned"

    @staticmethod
    def active() -> 'CustomerStatus':
        return CustomerStatus("active")

    @staticmethod
    def suspended() -> 'CustomerStatus':
        return CustomerStatus("suspended")

# ACL Translator — converts between legacy and new domain
class CustomerTranslator:
    """Translates between legacy data structures and new domain model."""

    @staticmethod
    def from_legacy(legacy_data: dict) -> Customer:
        """Translate legacy API response to domain Customer."""
        # Legacy uses 'cust_id', 'email_addr', 'first_nm', 'last_nm', 'stat_cd'
        # New domain uses 'id', 'email', 'full_name', 'status'
        full_name = f"{legacy_data.get('first_nm', '')} {legacy_data.get('last_nm', '')}".strip()

        # Legacy status codes: 1=active, 2=suspended, 3=churned
        status_map = {"1": "active", "2": "suspended", "3": "churned"}
        status = status_map.get(legacy_data.get("stat_cd", "1"), "active")

        return Customer(
            id=legacy_data["cust_id"],
            email=legacy_data["email_addr"].lower(),
            full_name=full_name,
            status=CustomerStatus(status),
            created_at=legacy_data.get("create_dt", "")
        )

    @staticmethod
    def to_legacy(customer: Customer) -> dict:
        """Translate domain Customer to legacy API format."""
        # Split full_name back into first/last for legacy
        parts = customer.full_name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        # Reverse status mapping
        status_map = {"active": "1", "suspended": "2", "churned": "3"}

        return {
            "cust_id": customer.id,
            "email_addr": customer.email,
            "first_nm": first_name,
            "last_nm": last_name,
            "stat_cd": status_map.get(customer.status.value, "1")
        }

# ACL Facade — the public interface the new domain uses
class CustomerACL:
    """Anti-corruption layer facade.
    The new domain calls this — never the legacy client directly."""

    def __init__(self, legacy_client: LegacyCustomerClient):
        self._legacy = legacy_client
        self._translator = CustomerTranslator()

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        legacy_data = self._legacy.fetch_customer(customer_id)
        if legacy_data is None:
            return None
        return self._translator.from_legacy(legacy_data)

    def create_customer(self, customer: Customer) -> Customer:
        legacy_data = self._translator.to_legacy(customer)
        result = self._legacy.insert_customer(legacy_data)
        return self._translator.from_legacy(result)

    def update_customer(self, customer: Customer) -> Customer:
        legacy_data = self._translator.to_legacy(customer)
        result = self._legacy.update_customer(customer.id, legacy_data)
        return self._translator.from_legacy(result)

    def suspend_customer(self, customer_id: str) -> Customer:
        legacy_data = self._legacy.update_status(customer_id, "2")
        return self._translator.from_legacy(legacy_data)
