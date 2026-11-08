"""Deep clone comparison: JSON round-trip vs copy.deepcopy.

The JSON path silently degrades types (datetime -> str, set -> list).
copy.deepcopy preserves everything, including circular references.
"""

import copy
import json
from datetime import datetime, timezone


def main() -> None:
    original = {
        "name": "config",
        "created": datetime(2026, 1, 1, tzinfo=timezone.utc),
        "tags": {"a", "b"},
        "nested": {"level": 2},
    }
    # circular reference: the object points back to itself
    original["self_ref"] = original

    print("== json round-trip (loses types) ==")
    try:
        json.loads(json.dumps(original))
    except (TypeError, ValueError) as exc:
        print(f"json.dumps failed: {type(exc).__name__}: circular ref not serializable")

    no_cycles = {k: v for k, v in original.items() if k != "self_ref"}
    try:
        json.loads(json.dumps(no_cycles))
    except TypeError as exc:
        print(f"json.dumps failed: {exc}  (datetime/set are not JSON types)")

    print("\n== copy.deepcopy (preserves everything) ==")
    clone = copy.deepcopy(original)
    print("created type preserved:", isinstance(clone["created"], datetime))
    print("tags type preserved:", isinstance(clone["tags"], set))
    print("nested is a copy:", clone["nested"] is not original["nested"])
    print("circular ref ok:", clone["self_ref"] is clone)

    clone["nested"]["level"] = 99
    print("original untouched:", original["nested"]["level"] == 2)


if __name__ == "__main__":
    main()
