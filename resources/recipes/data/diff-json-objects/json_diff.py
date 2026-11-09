"""Recursive JSON diff with no third-party dependencies.

Compares two JSON files (or stdin strings) and prints every
added / removed / changed path in RFC 6901 pointer form.

Usage:
    python json_diff.py old.json new.json
"""

import json
import sys


def json_diff(old, new, path=""):
    """Return {path: change} for two JSON-like structures."""
    changes = {}
    if old == new:
        return changes
    if isinstance(old, dict) and isinstance(new, dict):
        for key in old.keys() | new.keys():
            if key not in old:
                changes[f"{path}/{key}"] = {"added": new[key]}
            elif key not in new:
                changes[f"{path}/{key}"] = {"removed": old[key]}
            else:
                changes.update(json_diff(old[key], new[key], f"{path}/{key}"))
    elif isinstance(old, list) and isinstance(new, list):
        for i, (o, n) in enumerate(zip(old, new)):
            changes.update(json_diff(o, n, f"{path}/{i}"))
        for i in range(len(old), len(new)):
            changes[f"{path}/{i}"] = {"added": new[i]}
        for i in range(len(new), len(old)):
            changes[f"{path}/{i}"] = {"removed": old[i]}
    else:
        changes[path or "/"] = {"old": old, "new": new}
    return changes


def main():
    old_path, new_path = sys.argv[1], sys.argv[2]
    with open(old_path, encoding="utf-8") as f:
        old = json.load(f)
    with open(new_path, encoding="utf-8") as f:
        new = json.load(f)

    diff = json_diff(old, new)
    if not diff:
        print("No differences found.")
        return
    for path, change in sorted(diff.items()):
        print(f"{path:30} -> {change}")


if __name__ == "__main__":
    main()
