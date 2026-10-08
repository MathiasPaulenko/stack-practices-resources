"""Role Pattern — runnable example.

Assign/revoke dynamic roles on a Person entity at runtime and check
capabilities through role objects. No dependencies beyond stdlib.

Run: python role_pattern.py
"""

from typing import Dict, List, Optional, Protocol
from dataclasses import dataclass, field
from datetime import datetime

class Role(Protocol):
    """Protocol for roles that can be attached to entities"""
    role_name: str

    def can_perform(self, action: str) -> bool:
        ...


@dataclass
class CustomerRole:
    role_name: str = "customer"
    loyalty_points: int = 0

    def can_perform(self, action: str) -> bool:
        return action in ["browse", "purchase", "review"]

    def earn_points(self, amount: int):
        self.loyalty_points += amount


@dataclass
class EmployeeRole:
    role_name: str = "employee"
    department: str = ""
    salary: float = 0.0

    def can_perform(self, action: str) -> bool:
        return action in ["browse", "inventory", "support", "refund"]

    def process_refund(self, order_id: str) -> str:
        return f"Refund processed for {order_id}"


@dataclass
class VendorRole:
    role_name: str = "vendor"
    company_name: str = ""
    commission_rate: float = 0.05

    def can_perform(self, action: str) -> bool:
        return action in ["list_products", "manage_inventory", "view_sales"]


class Person:
    """Core entity that can hold multiple roles"""
    def __init__(self, person_id: str, name: str):
        self.person_id = person_id
        self.name = name
        self._roles: Dict[str, Role] = {}
        self._role_history: List[dict] = []

    def assign_role(self, role: Role):
        self._roles[role.role_name] = role
        self._role_history.append({
            "action": "assigned",
            "role": role.role_name,
            "timestamp": datetime.now().isoformat()
        })

    def revoke_role(self, role_name: str):
        if role_name in self._roles:
            del self._roles[role_name]
            self._role_history.append({
                "action": "revoked",
                "role": role_name,
                "timestamp": datetime.now().isoformat()
            })

    def has_role(self, role_name: str) -> bool:
        return role_name in self._roles

    def get_role(self, role_name: str) -> Optional[Role]:
        return self._roles.get(role_name)

    def can_perform(self, action: str) -> bool:
        return any(role.can_perform(action) for role in self._roles.values())

    @property
    def roles(self) -> List[str]:
        return list(self._roles.keys())


# Usage
person = Person("P-001", "Alice")
person.assign_role(CustomerRole(loyalty_points=100))
person.assign_role(EmployeeRole(department="Sales", salary=75000))

print(f"Alice's roles: {person.roles}")
print(f"Can browse: {person.can_perform('browse')}")
print(f"Can refund: {person.can_perform('refund')}")
print(f"Can list products: {person.can_perform('list_products')}")

# Access role-specific behavior
emp_role = person.get_role("employee")
if emp_role:
    print(emp_role.process_refund("ORD-123"))

# Revoke a role
person.revoke_role("customer")
print(f"Roles after revoke: {person.roles}")
