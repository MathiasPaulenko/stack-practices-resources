#!/usr/bin/env python3
"""Audit container/K8s manifests for immutability violations.

Checks (stdlib only, no YAML parser needed):
  - image tags using :latest or unpinned (no digest/tag)
  - missing readOnlyRootFilesystem
  - writable hostPath volumes
  - SSH ports exposed (22)
  - :latest in docker-compose files

Usage:
  python check_immutable.py deployment.yaml [more.yaml ...]
  python check_immutable.py --demo          # runs against a built-in sample
"""
import re
import sys

VIOLATIONS = [
    ("LATEST_TAG", re.compile(r"image:\s*\S+:latest\b"), "image uses :latest tag (mutable)"),
    ("WRITABLE_ROOTFS", re.compile(r"readOnlyRootFilesystem:\s*false"), "root filesystem is writable"),
    ("SSH_PORT", re.compile(r"[Pp]ort:\s*22\b|\"22(:|/)|- 22:"), "SSH port exposed (immutable = no shell access)"),
    ("HOSTPATH", re.compile(r"hostPath:"), "hostPath volume mounts host state into the container"),
    ("PRIVILEGED", re.compile(r"privileged:\s*true"), "privileged container can mutate the host"),
]


def check(text: str, name: str) -> list[str]:
    findings = []
    for key, pat, msg in VIOLATIONS:
        for i, line in enumerate(text.splitlines(), 1):
            if pat.search(line):
                findings.append(f"{name}:{i} [{key}] {msg}: {line.strip()[:80]}")
    # A file with containers but no readOnlyRootFilesystem at all
    if "containers:" in text and "readOnlyRootFilesystem" not in text:
        findings.append(f"{name}:0 [NO_READONLY_ROOTFS] no readOnlyRootFilesystem set anywhere")
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"image:\s*\S+", line) and "@sha256:" not in line:
            findings.append(f"{name}:{i} [NO_DIGEST] image not pinned by digest: {line.strip()[:80]}")
    return findings


DEMO = """apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: api
        image: myregistry.com/api:latest
        ports:
        - containerPort: 22
        securityContext:
          privileged: true
"""


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] == "--demo":
        targets = [("demo.yaml", DEMO)]
    else:
        targets = []
        for path in args:
            try:
                targets.append((path, open(path, encoding="utf-8").read()))
            except OSError as e:
                print(f"cannot read {path}: {e}", file=sys.stderr)
                return 2

    total = 0
    for name, text in targets:
        findings = check(text, name)
        total += len(findings)
        for f in findings:
            print(f)
        if not findings:
            print(f"{name}: OK (no immutability violations)")
    print(f"\n{total} violation(s) across {len(targets)} file(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
