"""flyweight_python.py — Flyweight pattern implementation in Python.

Run: python flyweight_python.py
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class TreeType:
    """Flyweight: shared intrinsic state (species, color, texture)."""
    species: str
    color: str
    texture: str

    _cache: ClassVar[dict] = {}

    @classmethod
    def get(cls, species: str, color: str, texture: str) -> "TreeType":
        key = (species, color, texture)
        if key not in cls._cache:
            cls._cache[key] = cls(species, color, texture)
        return cls._cache[key]

    @classmethod
    def cache_size(cls) -> int:
        return len(cls._cache)

    def render(self, x: int, y: int) -> str:
        return f"Rendering {self.species} at ({x}, {y}) color={self.color}"


@dataclass
class Tree:
    """Context: holds extrinsic state (x, y) and a reference to the flyweight."""
    x: int
    y: int
    tree_type: TreeType

    def render(self) -> str:
        return self.tree_type.render(self.x, self.y)


def build_forest(n: int = 1000) -> list[Tree]:
    """Build a forest of n trees sharing a single TreeType."""
    tree_type = TreeType.get("Oak", "green", "bark.png")
    return [Tree(i, i, tree_type) for i in range(n)]


def build_mixed_forest(n: int = 1000) -> list[Tree]:
    """Build a forest with multiple shared TreeType instances."""
    types = [
        TreeType.get("Oak", "green", "bark.png"),
        TreeType.get("Pine", "dark", "pine.png"),
        TreeType.get("Birch", "light", "birch.png"),
    ]
    return [Tree(i, i, types[i % len(types)]) for i in range(n)]


if __name__ == "__main__":
    forest = build_forest(1000)
    print(forest[0].render())
    print(forest[999].render())
    print(f"Unique tree types: {TreeType.cache_size()}")

    mixed = build_mixed_forest(3000)
    print(f"\nMixed forest: {len(mixed)} trees, {TreeType.cache_size()} unique types")
