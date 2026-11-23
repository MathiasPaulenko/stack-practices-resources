"""Null Object pattern in Python: User interface + NullUser + NullLogger demo."""
from abc import ABC, abstractmethod


class User(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def has_access(self, resource: str) -> bool:
        pass

    @abstractmethod
    def get_permissions(self) -> list:
        pass


class RealUser(User):
    def __init__(self, name, permissions=None):
        self.name = name
        self.permissions = permissions or []

    def get_name(self):
        return self.name

    def has_access(self, resource):
        return resource in self.permissions

    def get_permissions(self):
        return self.permissions


class NullUser(User):
    """Null object with safe default behavior."""

    def get_name(self):
        return "Guest"

    def has_access(self, resource):
        return False

    def get_permissions(self):
        return []


def find_user(user_id):
    # Simulated lookup
    if user_id == 1:
        return RealUser("Alice", ["reports", "settings"])
    return NullUser()  # No null, no crash


if __name__ == "__main__":
    user = find_user(999)
    print(user.get_name())           # Guest
    print(user.has_access("admin"))  # False
    print(user.get_permissions())    # []
