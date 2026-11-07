"""Cycle-checking add() for the Composite Pattern.

A SafeFolder validates that a new child is not already inside its own
subtree before inserting, so get_size() can never recurse forever.

Run: python test_cycle_check.py  (uses unittest, no pytest needed)
"""
import unittest


class Component:
    def get_size(self) -> int:
        raise NotImplementedError


class File(Component):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size


class SafeFolder(Component):
    def __init__(self, name: str):
        self.name = name
        self.children: list[Component] = []

    def _contains(self, node: Component) -> bool:
        # True if `node` is this folder or lives in its subtree.
        if node is self:
            return True
        return any(
            child._contains(node) if isinstance(child, SafeFolder) else child is node
            for child in self.children
        )

    def add(self, component: Component):
        # Reject if the new child is this folder itself or already
        # contains it in its subtree — either would make get_size() recurse forever.
        if component is self or (
            isinstance(component, SafeFolder) and component._contains(self)
        ):
            raise ValueError(f"cycle rejected: adding {component!r} to {self.name}")
        self.children.append(component)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)


class CycleCheckTests(unittest.TestCase):
    def test_direct_self_add_is_rejected(self):
        folder = SafeFolder("root")
        with self.assertRaises(ValueError):
            folder.add(folder)

    def test_indirect_cycle_is_rejected(self):
        root = SafeFolder("root")
        child = SafeFolder("child")
        root.add(child)
        with self.assertRaises(ValueError):
            child.add(root)  # would create root -> child -> root

    def test_legitimate_add_works(self):
        root = SafeFolder("root")
        root.add(File("a.txt", 10))
        root.add(SafeFolder("sub"))
        self.assertEqual(root.get_size(), 10)

    def test_empty_folder_is_zero(self):
        self.assertEqual(SafeFolder("empty").get_size(), 0)


if __name__ == "__main__":
    unittest.main()
