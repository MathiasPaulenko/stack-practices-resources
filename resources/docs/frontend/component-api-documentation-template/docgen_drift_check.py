#!/usr/bin/env python3
"""Drift check: react-docgen output vs documented props table.

Usage:
    npx react-docgen src/components/Button/Button.tsx --pretty > docgen.json
    python docgen_drift_check.py docgen.json component-api-doc.md

Exit code 0 = doc matches code. Exit code 1 = drift (prints the diff).
Stdlib only.
"""

import json
import re
import sys

PROPS_HEADING = "Props"  # adjust if your template uses a translated heading


def docgen_props(path):
    """Return the set of prop names from a react-docgen JSON file."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    # react-docgen emits a single component object (has "props"), a dict keyed
    # by file path, or a list of component objects.
    if isinstance(data, dict) and "props" in data:
        components = [data]
    elif isinstance(data, dict):
        components = list(data.values())
    else:
        components = data
    props = set()
    for comp in components:
        if isinstance(comp, dict) and isinstance(comp.get("props"), dict):
            props.update(comp["props"].keys())
    return props


def documented_props(path):
    """Return prop names from the first column of the `## Props` markdown table."""
    in_props = False
    props = set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if re.match(r"^##\s+", line):
                in_props = line.lstrip("# ").strip() == PROPS_HEADING
                continue
            if not in_props:
                continue
            row = re.match(r"^\|\s*`?(\w[\w-]*)`?\s*\|", line)
            if row:
                name = row.group(1)
                if name.lower() not in ("prop", "------"):  # skip header/separator
                    props.add(name)
            elif line.strip() and not line.lstrip().startswith("|"):
                in_props = False  # table ended
    return props


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: docgen_drift_check.py <docgen.json> <component-doc.md>")

    code_props = docgen_props(sys.argv[1])
    doc_props = documented_props(sys.argv[2])

    missing_in_doc = sorted(code_props - doc_props)
    stale_in_doc = sorted(doc_props - code_props)

    if not missing_in_doc and not stale_in_doc:
        print(f"OK: {len(doc_props)} documented props match the source.")
        return

    for name in missing_in_doc:
        print(f"MISSING IN DOC : {name}")
    for name in stale_in_doc:
        print(f"STALE IN DOC   : {name}  (not found in source)")
    sys.exit(1)


if __name__ == "__main__":
    main()
