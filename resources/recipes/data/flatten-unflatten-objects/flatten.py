"""Flatten and unflatten nested objects in Python.

Usage:
    python flatten.py
"""

import json
import re
from typing import Any


def flatten(obj: Any, separator: str = ".", prefix: str = "") -> dict:
    result = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key
            result.update(flatten(value, separator, new_key))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            new_key = f"{prefix}[{index}]"
            result.update(flatten(value, separator, new_key))
    else:
        result[prefix] = obj
    return result


def _set(node, parts, value):
    for i, part in enumerate(parts[:-1]):
        next_is_index = parts[i + 1].isdigit()
        if isinstance(node, list):
            index = int(part)
            while len(node) <= index:
                node.append(None)
            if node[index] is None:
                node[index] = [] if next_is_index else {}
            node = node[index]
        else:
            if part not in node:
                node[part] = [] if next_is_index else {}
            node = node[part]

    last = parts[-1]
    if isinstance(node, list):
        index = int(last)
        while len(node) <= index:
            node.append(None)
        node[index] = value
    else:
        node[last] = value


def unflatten(flat: dict, separator: str = ".") -> Any:
    result = {}
    split_re = re.compile(re.escape(separator) + r"|\[|\]")
    for key, value in flat.items():
        parts = [p for p in split_re.split(key) if p]
        _set(result, parts, value)
    return result


if __name__ == "__main__":
    with open("sample.json") as f:
        nested = json.load(f)

    flat = flatten(nested)
    print("=== Flattened ===")
    for key, value in flat.items():
        print(f"  {key}: {value}")

    restored = unflatten(flat)
    print("\n=== Unflattened ===")
    print(json.dumps(restored, indent=2))

    # Verify round-trip
    flat_again = flatten(restored)
    assert flat == flat_again, "Round-trip failed!"
    print("\n✓ Round-trip verified: flatten(unflatten(flat)) == flat")
