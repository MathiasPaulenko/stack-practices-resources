"""test_flyweight.py — Unit tests for the Flyweight pattern examples.

Run: python -m pytest test_flyweight.py -v
"""
import pytest
from flyweight_python import TreeType, Tree, build_forest, build_mixed_forest


class TestTreeType:
    def test_same_intrinsic_state_returns_same_instance(self):
        a = TreeType.get("Oak", "green", "bark.png")
        b = TreeType.get("Oak", "green", "bark.png")
        assert a is b

    def test_different_intrinsic_state_returns_different_instance(self):
        a = TreeType.get("Oak", "green", "bark.png")
        b = TreeType.get("Pine", "dark", "pine.png")
        assert a is not b

    def test_is_immutable(self):
        tree_type = TreeType.get("Oak", "green", "bark.png")
        with pytest.raises(Exception):
            tree_type.species = "Pine"

    def test_render_returns_correct_string(self):
        tree_type = TreeType.get("Oak", "green", "bark.png")
        result = tree_type.render(10, 20)
        assert "Oak" in result
        assert "10" in result
        assert "20" in result

    def test_cache_size_increases_with_unique_keys(self):
        initial = TreeType.cache_size()
        TreeType.get("Cedar", "brown", "cedar.png")
        assert TreeType.cache_size() >= initial + 1


class TestTree:
    def test_tree_holds_extrinsic_state(self):
        tree_type = TreeType.get("Oak", "green", "bark.png")
        tree = Tree(5, 10, tree_type)
        assert tree.x == 5
        assert tree.y == 10
        assert tree.tree_type is tree_type

    def test_tree_render_delegates_to_flyweight(self):
        tree_type = TreeType.get("Oak", "green", "bark.png")
        tree = Tree(5, 10, tree_type)
        result = tree.render()
        assert "Oak" in result
        assert "(5, 10)" in result


class TestForest:
    def test_build_forest_shares_single_type(self):
        forest = build_forest(100)
        assert len(forest) == 100
        first_type = forest[0].tree_type
        assert all(t.tree_type is first_type for t in forest)

    def test_build_mixed_forest_shares_three_types(self):
        forest = build_mixed_forest(300)
        assert len(forest) == 300
        unique_types = {id(t.tree_type) for t in forest}
        assert len(unique_types) == 3

    def test_build_forest_memory_efficiency(self):
        forest = build_forest(1000)
        unique_types = {id(t.tree_type) for t in forest}
        assert len(unique_types) == 1
        assert len(forest) == 1000
