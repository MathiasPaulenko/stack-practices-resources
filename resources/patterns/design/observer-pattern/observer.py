"""Observer pattern: a subject notifies subscribed observers on every event."""
from __future__ import annotations

from typing import Callable, List


class Subject:
    """Holds a list of observer callables and fans events out to them."""

    def __init__(self) -> None:
        self._observers: List[Callable[[str], None]] = []

    def attach(self, observer: Callable[[str], None]) -> Callable[[], None]:
        """Subscribe and return an unsubscribe callable — call it in teardown."""
        self._observers.append(observer)

        def unsubscribe() -> None:
            if observer in self._observers:
                self._observers.remove(observer)

        return unsubscribe

    def notify(self, data: str) -> None:
        for observer in self._observers:
            try:
                observer(data)
            except Exception as exc:  # one bad observer must not break the rest
                print(f"Observer error: {exc}")


if __name__ == "__main__":
    subject = Subject()
    subject.attach(lambda d: print(f"A received: {d}"))
    unsubscribe_b = subject.attach(lambda d: print(f"B received: {d}"))

    subject.notify("Hello observers!")
    unsubscribe_b()
    subject.notify("B is gone")
