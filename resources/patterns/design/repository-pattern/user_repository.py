"""Repository Pattern — Python implementation."""
from abc import ABC, abstractmethod
from typing import Optional


class User:
    def __init__(self, id: int, name: str, role: str = "member"):
        self.id = id
        self.name = name
        self.role = role

    def __eq__(self, other):
        return isinstance(other, User) and self.id == other.id

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r}, role={self.role!r})"


class UserRepository(ABC):
    """Abstract repository interface — the contract."""

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[User]:
        ...

    @abstractmethod
    def find_all(self) -> list[User]:
        ...

    @abstractmethod
    def save(self, user: User) -> None:
        ...

    @abstractmethod
    def delete(self, id: int) -> bool:
        ...


class InMemoryUserRepository(UserRepository):
    """In-memory implementation for fast, deterministic unit tests."""

    def __init__(self):
        self._users: dict[int, User] = {}

    def get_by_id(self, id: int) -> Optional[User]:
        return self._users.get(id)

    def find_all(self) -> list[User]:
        return list(self._users.values())

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def delete(self, id: int) -> bool:
        return self._users.pop(id, None) is not None


class UserService:
    """Domain service — depends on the interface, not the concrete class."""

    def __init__(self, repo: UserRepository):
        self._repo = repo

    def promote_user(self, id: int) -> User:
        user = self._repo.get_by_id(id)
        if user is None:
            raise ValueError("User not found")
        user.role = "admin"
        self._repo.save(user)
        return user
