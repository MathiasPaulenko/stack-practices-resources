"""Modular monolith boundary linter.

Rule: a module may import another module's `api` package and `shared.kernel`.
Nothing else may cross a module boundary — that's the whole architecture.

Layout expected:
    modules/<name>/{domain,application,infrastructure,api}/...
    shared/kernel/...
"""
import re
import sys
import unittest
from pathlib import Path

IMPORT_RE = re.compile(r"^(?:from|import)\s+([\w.]+)", re.M)
TOP_LEVEL = {"modules", "shared"}


def module_of(dotted: str):
    """Return ('module', name, 'internal'|'api'|'kernel') for a dotted import."""
    parts = dotted.split(".")
    if parts[:2] == ["shared", "kernel"]:
        return ("kernel", "kernel", "kernel")
    if len(parts) >= 3 and parts[0] == "modules":
        kind = "api" if parts[2] == "api" else "internal"
        return ("module", parts[1], kind)
    return (None, None, None)


def check_boundaries(root: Path):
    """Return list of violations: (file, line_no, import, reason)."""
    violations = []
    for py_file in sorted(root.rglob("*.py")):
        rel = py_file.relative_to(root)
        src_module = module_of(".".join(rel.with_suffix("").parts))
        if src_module[0] not in ("module", "kernel"):
            continue
        text = py_file.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), 1):
            m = IMPORT_RE.match(line.strip())
            if not m:
                continue
            dst = module_of(m.group(1))
            if dst[0] == "kernel":
                continue
            if dst[0] != "module" or dst[1] == src_module[1]:
                continue
            if dst[2] != "api":
                violations.append(
                    (str(rel), lineno, m.group(1),
                     f"{src_module[1]} reaches into {dst[1]}'s internals "
                     f"(only '{dst[1]}.api' is public)")
                )
    return violations


def report(violations) -> str:
    if not violations:
        return "Boundaries intact: all cross-module imports go through public APIs."
    lines = ["Boundary violations:"]
    for f, line, imp, why in violations:
        lines.append(f"  {f}:{line}  import {imp}  — {why}")
    return "\n".join(lines)


def _write(root: Path, rel: str, text: str):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


class BoundaryCheckTest(unittest.TestCase):
    def test_ignores_kernel_and_same_module_imports(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write(root, "modules/orders/application/place_order.py",
                   "from shared.kernel.domain_event import DomainEvent\n"
                   "from modules.orders.domain.order import Order\n")
            self.assertEqual(check_boundaries(root), [])

    def test_allows_api_imports(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write(root, "modules/orders/application/place_order.py",
                   "from modules.catalog.api.catalog_api import CatalogApi\n")
            self.assertEqual(check_boundaries(root), [])

    def test_flags_internal_imports(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write(root, "modules/orders/application/place_order.py",
                   "from modules.catalog.infrastructure.product_repository import ProductRepository\n")
            v = check_boundaries(root)
            self.assertEqual(len(v), 1)
            self.assertIn("orders reaches into catalog's internals", v[0][3])

    def test_flags_kernel_import_from_other_direction(self):
        # kernel is allowed both ways — sanity that we don't over-flag
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write(root, "shared/kernel/money.py", "")
            _write(root, "modules/catalog/domain/product.py",
                   "from shared.kernel.money import Money\n")
            self.assertEqual(check_boundaries(root), [])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        v = check_boundaries(Path(sys.argv[1]))
        print(report(v))
        sys.exit(1 if v else 0)
    unittest.main(verbosity=2)
