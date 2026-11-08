"""Validate a Data Mesh data product spec and its Avro schema.

Runs with the standard library only for the .avsc JSON schema; installs
pyyaml if you also want spec validation (pip install pyyaml).

Usage:
    python validate_product.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent

REQUIRED_SPEC_FIELDS = {"name", "owner", "schema", "quality", "access"}
REQUIRED_QUALITY_FIELDS = {"freshness_sla", "completeness"}


def validate_avro_schema(path: Path) -> list[str]:
    """Check the .avsc file parses and has the fields the producer emits."""
    errors: list[str] = []
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.name}: invalid JSON — {exc}"]

    if schema.get("type") != "record":
        errors.append(f"{path.name}: top-level type must be 'record'")

    field_names = {f["name"] for f in schema.get("fields", [])}
    emitted = {"order_id", "event_type", "customer_id", "total", "occurred_at"}
    missing = emitted - field_names
    if missing:
        errors.append(f"{path.name}: producer emits fields missing from schema: {sorted(missing)}")

    pii = [f["name"] for f in schema.get("fields", []) if "PII" in f.get("doc", "")]
    if not pii:
        errors.append(f"{path.name}: no field documented as PII")
    return errors


def validate_product_spec(path: Path) -> list[str]:
    """Check the data-product.yaml spec has the fields the catalog requires."""
    try:
        import yaml  # pyyaml — optional dependency
    except ImportError:
        return [f"{path.name}: skipped (pip install pyyaml to enable spec validation)"]

    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    missing = REQUIRED_SPEC_FIELDS - spec.keys()
    if missing:
        errors.append(f"{path.name}: missing required fields: {sorted(missing)}")

    owner = spec.get("owner", "")
    if "@" not in owner or owner.endswith("@company.com") is False:
        errors.append(f"{path.name}: owner should be a team email, got {owner!r}")

    quality_missing = REQUIRED_QUALITY_FIELDS - spec.get("quality", {}).keys()
    if quality_missing:
        errors.append(f"{path.name}: missing SLA fields: {sorted(quality_missing)}")

    if not spec.get("access", {}).get("pii_fields"):
        errors.append(f"{path.name}: pii_fields is empty — tag PII or set classification accordingly")
    return errors


def main() -> int:
    errors = validate_avro_schema(ROOT / "schemas" / "order_event.avsc")
    errors += validate_product_spec(ROOT / "data-product.yaml")
    for e in errors:
        print(f"FAIL {e}")
    if not errors:
        print("OK — data product spec and Avro schema are consistent")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
