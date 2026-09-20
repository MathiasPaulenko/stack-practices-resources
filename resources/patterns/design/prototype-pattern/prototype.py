"""Prototype pattern — a named registry of clonable objects.

`PrototypeRegistry` maps keys to configured prototype instances and hands
out a fresh deep clone on every `get()`. Callers never see a concrete
class or constructor — just a key and an independent copy.

Run the demo:   python prototype.py
Run the tests:  python -m pytest test_prototype.py -v
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProductConfig:
    """A configurable prototype: nested structures must not leak between clones."""

    name: str
    price: float
    category: str
    attributes: dict[str, str] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    def clone(self) -> "ProductConfig":
        # deepcopy so `attributes` and `tags` stay independent per clone
        return copy.deepcopy(self)

    def set_attribute(self, key: str, value: str) -> "ProductConfig":
        self.attributes[key] = value
        return self

    def add_tag(self, tag: str) -> "ProductConfig":
        self.tags.append(tag)
        return self


class PrototypeRegistry:
    """Map of name -> configured prototype. Every lookup returns a clone."""

    def __init__(self) -> None:
        self._prototypes: dict[str, Any] = {}

    def register(self, key: str, prototype: Any) -> None:
        if not hasattr(prototype, "clone"):
            raise TypeError(f"Prototype '{key}' must implement clone()")
        self._prototypes[key] = prototype

    def get(self, key: str) -> Any:
        proto = self._prototypes.get(key)
        return proto.clone() if proto is not None else None

    def keys(self) -> list[str]:
        return list(self._prototypes)


def _demo() -> None:
    registry = PrototypeRegistry()
    registry.register(
        "pro",
        ProductConfig(
            "Pro", 29.99, "software", {"tier": "pro", "support": "24h"}, ["pro", "priority"]
        ),
    )

    custom = registry.get("pro")
    custom.name = "Pro Custom"
    custom.set_attribute("discount", "20%").add_tag("custom")

    original = registry.get("pro")
    print(f"custom:   {custom.name} attrs={custom.attributes} tags={custom.tags}")
    print(f"original: {original.name} attrs={original.attributes} tags={original.tags}")
    print(f"independent: {custom.attributes is not original.attributes}")


if __name__ == "__main__":
    _demo()
