"""Mediator pattern: chat room. Run: python chat_room.py"""
from abc import ABC, abstractmethod


class ChatMediator(ABC):
    @abstractmethod
    def send_message(self, message: str, sender: "User") -> None: ...

    @abstractmethod
    def add_user(self, user: "User") -> None: ...


class ChatRoom(ChatMediator):
    def __init__(self) -> None:
        self.users: list[User] = []

    def add_user(self, user: "User") -> None:
        self.users.append(user)

    def send_message(self, message: str, sender: "User") -> None:
        for user in self.users:
            if user != sender:
                user.receive(message, sender.name)


class User:
    def __init__(self, name: str, mediator: ChatMediator) -> None:
        self.name = name
        self.mediator = mediator
        mediator.add_user(self)

    def send(self, message: str) -> None:
        print(f"{self.name} sends: {message}")
        self.mediator.send_message(message, self)

    def receive(self, message: str, from_name: str) -> None:
        print(f"{self.name} receives from {from_name}: {message}")


if __name__ == "__main__":
    room = ChatRoom()
    alice = User("Alice", room)
    bob = User("Bob", room)
    alice.send("Hello everyone!")
