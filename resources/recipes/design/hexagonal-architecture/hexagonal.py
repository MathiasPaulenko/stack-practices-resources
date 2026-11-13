"""Python variant of the hexagonal architecture example.

Ports are declared as ABCs, adapters as plain classes. The domain imports
nothing but the standard library.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import uuid


class UserRepository(ABC):
    """Secondary port: persistence the domain needs."""

    @abstractmethod
    async def find_by_id(self, id: str) -> Optional["User"]:
        ...

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional["User"]:
        ...

    @abstractmethod
    async def save(self, user: "User") -> None:
        ...


class EmailService(ABC):
    """Secondary port: notification capability the domain needs."""

    @abstractmethod
    async def send(self, user: "User", subject: str, body: str) -> None:
        ...


@dataclass
class User:
    id: str
    email: str
    name: str
    is_verified: bool = False

    def verify(self) -> None:
        self.is_verified = True


class UserRegistrationService:
    def __init__(self, users: UserRepository, email: EmailService):
        self._users = users
        self._email = email

    async def register(self, email: str, name: str) -> User:
        existing = await self._users.find_by_email(email)
        if existing:
            raise ValueError("User already exists")

        user = User(id=str(uuid.uuid4()), email=email, name=name)
        await self._users.save(user)
        await self._email.send(user, "Welcome", f"Hello {name}, welcome aboard!")
        return user

    async def verify_email(self, user_id: str) -> None:
        user = await self._users.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        user.verify()
        await self._users.save(user)


# Driven adapter example: in-memory repository for tests.
class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    async def find_by_id(self, id: str) -> Optional[User]:
        return self._users.get(id)

    async def find_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self._users.values() if u.email == email), None)

    async def save(self, user: User) -> None:
        self._users[user.id] = user
