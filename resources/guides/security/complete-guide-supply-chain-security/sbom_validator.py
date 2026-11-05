"""Validate a CycloneDX SBOM: license compliance and outdated components.

Usage:
    python sbom_validator.py sbom.json
"""
import json
import sys


class SBOMValidator:
    def __init__(self, sbom_path: str):
        with open(sbom_path) as f:
            self.sbom = json.load(f)

    def get_components(self) -> list:
        return self.sbom.get("components", [])

    def find_component(self, name: str) -> dict | None:
        for comp in self.get_components():
            if comp["name"] == name:
                return comp
        return None

    def check_license_compliance(self, allowed_licenses: set) -> list:
        violations = []
        for comp in self.get_components():
            licenses = comp.get("licenses", [])
            for lic in licenses:
                lic_id = lic.get("license", {}).get("id", "")
                if lic_id and lic_id not in allowed_licenses:
                    violations.append({
                        "component": comp["name"],
                        "version": comp["version"],
                        "license": lic_id,
                    })
        return violations

    def check_outdated(self, latest_versions: dict) -> list:
        outdated = []
        for comp in self.get_components():
            name = comp["name"]
            current = comp["version"]
            latest = latest_versions.get(name)
            if latest and current != latest:
                outdated.append({
                    "component": name,
                    "current": current,
                    "latest": latest,
                })
        return outdated


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "sbom.json"
    validator = SBOMValidator(path)

    allowed = {"MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "MPL-2.0"}
    violations = validator.check_license_compliance(allowed)
    for v in violations:
        print(f"License violation: {v['component']} uses {v['license']}")

    latest = {"requests": "2.32.0", "flask": "3.0.3"}
    outdated = validator.check_outdated(latest)
    for o in outdated:
        print(f"Outdated: {o['component']} {o['current']} -> {o['latest']}")
