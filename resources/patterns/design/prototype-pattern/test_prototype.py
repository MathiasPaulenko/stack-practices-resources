"""Tests for the prototype registry.

Run:  python -m pytest test_prototype.py -v
"""
import pytest

from prototype import ProductConfig, PrototypeRegistry


def make_registry():
    registry = PrototypeRegistry()
    registry.register(
        "pro",
        ProductConfig("Pro", 29.99, "software", {"tier": "pro"}, ["pro", "priority"]),
    )
    return registry


def test_clone_is_a_new_object_with_equal_state():
    original = ProductConfig("Pro", 29.99, "software", {"tier": "pro"}, ["pro"])
    clone = original.clone()
    assert clone is not original
    assert clone.name == original.name
    assert clone.attributes == original.attributes


def test_clone_is_deep_nested_structures_are_independent():
    original = ProductConfig("Pro", 29.99, "software", {"tier": "pro"}, ["pro"])
    clone = original.clone()
    clone.attributes["discount"] = "20%"
    clone.tags.append("custom")
    assert "discount" not in original.attributes
    assert "custom" not in original.tags


def test_registry_returns_independent_clones():
    registry = make_registry()
    a = registry.get("pro")
    b = registry.get("pro")
    a.add_tag("mutated")
    assert "mutated" not in b.tags


def test_registered_prototype_is_not_mutated_by_clones():
    registry = make_registry()
    custom = registry.get("pro")
    custom.name = "Custom"
    custom.attributes.clear()
    fresh = registry.get("pro")
    assert fresh.name == "Pro"
    assert fresh.attributes == {"tier": "pro"}


def test_unknown_key_returns_none():
    assert make_registry().get("missing") is None


def test_register_rejects_non_clonable():
    registry = PrototypeRegistry()
    with pytest.raises(TypeError):
        registry.register("bad", object())
