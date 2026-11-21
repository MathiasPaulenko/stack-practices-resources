"""Merge JSON files: array concat, safe deep merge, glob multi-merge, dedupe."""
import copy
import glob
import json
from pathlib import Path


def deep_merge(base, override):
    """Deep-merge two dicts without mutating the inputs."""
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def merge_arrays(data_dir):
    merged = []
    for f in sorted(Path(data_dir).glob("*.json")):
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
            merged.extend(data) if isinstance(data, list) else merged.append(data)
    return merged


def merge_json_glob(pattern, output):
    merged = {}
    for filepath in sorted(glob.glob(pattern)):
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                merged.update(data)
            elif isinstance(data, list):
                merged.setdefault("items", []).extend(data)
    with open(output, "w", encoding="utf-8") as out:
        json.dump(merged, out, indent=2, ensure_ascii=False)


def merge_and_dedupe(files, key="id"):
    seen, merged = set(), []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            for item in json.load(fh):
                if item.get(key) not in seen:
                    seen.add(item[key])
                    merged.append(item)
    return merged


if __name__ == "__main__":
    base = {"db": {"host": "x", "port": 5432}, "name": "app"}
    override = {"db": {"port": 3306}, "debug": True}
    print(json.dumps(deep_merge(base, override), indent=2))
    # base is untouched: mutation-free merge
    assert base["db"]["port"] == 5432
