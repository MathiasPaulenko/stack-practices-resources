from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    email: str
    is_active: bool = True

    def can_login(self) -> bool:
        return self.is_active
