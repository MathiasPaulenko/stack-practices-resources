# Chain of Responsibility Pattern — runnable demo
# Usage: python chain.py
from abc import ABC, abstractmethod
from typing import Optional

class Handler(ABC):
    def __init__(self):
        self._next: Optional['Handler'] = None

    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: str) -> Optional[str]:
        pass

    def _pass_to_next(self, request: str) -> Optional[str]:
        if self._next:
            return self._next.handle(request)
        return None

class AuthHandler(Handler):
    def handle(self, request: str) -> Optional[str]:
        if not request.startswith("token:"):
            return "401 Unauthorized"
        return self._pass_to_next(request)

class RateLimitHandler(Handler):
    def __init__(self):
        super().__init__()
        self.requests = 0
        self.limit = 3

    def handle(self, request: str) -> Optional[str]:
        self.requests += 1
        if self.requests > self.limit:
            return "429 Too Many Requests"
        return self._pass_to_next(request)

class DataHandler(Handler):
    def handle(self, request: str) -> Optional[str]:
        return f"Processed: {request}"

handler = AuthHandler()
handler.set_next(RateLimitHandler()).set_next(DataHandler())

print(handler.handle("token:abc123"))  # Processed
print(handler.handle("bad-request"))   # 401
