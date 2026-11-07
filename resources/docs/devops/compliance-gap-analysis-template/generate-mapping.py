#!/usr/bin/env python3
"""Multi-framework control mapping generator.

Extends FRAMEWORK_MAPPING with your own controls and requirement IDs,
then run: python generate-mapping.py > multi-framework-mapping.md
"""
from pathlib import Path

FRAMEWORK_MAPPING = {
    "MFA enforcement": {
        "soc2": "CC6.1",
        "iso27001": "A.9.4.2",
        "pci": "8.3.1",
        "control": "Multi-factor authentication for all privileged accounts",
        "evidence": ["IAM MFA config", "Enrollment report", "Root MFA status"],
    },
    "Encryption at rest": {
        "soc2": "CC6.7",
        "iso27001": "A.10.1.1",
        "pci": "3.4",
        "control": "AES-256 encryption for all data stores",
        "evidence": ["KMS key policy", "S3 encryption config", "RDS encryption status"],
    },
    "Centralized logging": {
        "soc2": "CC7.2",
        "iso27001": "A.12.4.1",
        "pci": "10.1",
        "control": "All systems forward logs to centralized SIEM",
        "evidence": ["SIEM ingestion config", "Log source inventory", "Retention policy"],
    },
    "Vulnerability scanning": {
        "soc2": "CC7.1",
        "iso27001": "A.12.6.1",
        "pci": "11.2",
        "control": "Quarterly vulnerability scans with remediation SLA",
        "evidence": ["Scanner reports", "Remediation tickets", "SLA document"],
    },
    "Access reviews": {
        "soc2": "CC6.3",
        "iso27001": "A.9.2.5",
        "pci": "8.2.4",
        "control": "Quarterly access reviews with documented attestation",
        "evidence": ["Review records", "Manager sign-off", "Removal tickets"],
    },
}


def generate_mapping_report(mapping: dict) -> str:
    lines = [
        "| Control | SOC 2 | ISO 27001 | PCI-DSS | Evidence |",
        "|---------|-------|-----------|---------|----------|",
    ]
    for name, data in mapping.items():
        evidence = ", ".join(data["evidence"])
        lines.append(
            f"| {name} | {data['soc2']} | {data['iso27001']} | "
            f"{data['pci']} | {evidence} |"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    report = generate_mapping_report(FRAMEWORK_MAPPING)
    Path("multi-framework-mapping.md").write_text(report)
    print(report)
