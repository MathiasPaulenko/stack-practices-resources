"""Factory Pattern: canonical notification example with a registry.

Callers ask for a channel and get back a Notification — they never see
the concrete class. New channels are added with register(), not by
editing the factory.
"""
from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"Sending email: {message}"


class SmsNotification(Notification):
    def send(self, message: str) -> str:
        return f"Sending SMS: {message}"


class PushNotification(Notification):
    def send(self, message: str) -> str:
        return f"Sending push: {message}"


class NotificationFactory:
    _registry = {
        "email": EmailNotification,
        "sms": SmsNotification,
    }

    @classmethod
    def create(cls, channel: str) -> Notification:
        try:
            return cls._registry[channel]()
        except KeyError:
            raise ValueError(f"Unknown channel: {channel}")

    @classmethod
    def register(cls, channel: str, product: type[Notification]) -> None:
        cls._registry[channel] = product


if __name__ == "__main__":
    notifier = NotificationFactory.create("email")
    print(notifier.send("Hello!"))

    # Registering a new channel doesn't touch the factory's create().
    NotificationFactory.register("push", PushNotification)
    push = NotificationFactory.create("push")
    print(push.send("Hello!"))
