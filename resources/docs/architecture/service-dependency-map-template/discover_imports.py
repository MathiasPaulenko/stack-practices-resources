"""Static dependency discovery: parse Python imports into a dependency set.

Catches compile-time dependencies but misses runtime ones (HTTP calls,
event consumers). Combine with tracing data for a complete picture.

Usage: python discover_imports.py <project_dir>
"""

import ast
import os
import sys


def find_dependencies(project_dir: str) -> set[str]:
    deps = set()
    for root, _, files in os.walk(project_dir):
        for f in files:
            if f.endswith(".py"):
                with open(os.path.join(root, f)) as fh:
                    tree = ast.parse(fh.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                deps.add(alias.name)
                        elif isinstance(node, ast.ImportFrom):
                            deps.add(node.module)
    return deps


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    for dep in sorted(find_dependencies(target)):
        print(dep)
