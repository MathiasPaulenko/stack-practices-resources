"""Generate, rotate and audit SSH keys in ~/.ssh via ssh-keygen.

Note the `ssh-keygen -lf` output format:
    <bits> <SHA256:fingerprint> <comment...> (<TYPE>)
The key type is the last field; the comment is everything in between.
"""

import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class SSHKeyInfo:
    key_type: str
    bits: int
    fingerprint: str
    comment: str
    file_path: str


class SSHKeyManager:
    """Generate, rotate and audit SSH keys in ~/.ssh."""

    def __init__(self, key_dir: str = "~/.ssh"):
        self.key_dir = Path(key_dir).expanduser()
        self.key_dir.mkdir(parents=True, exist_ok=True)
        self.key_dir.chmod(0o700)

    def generate_key(self, name: str, key_type: str = "ed25519",
                     passphrase: str = "", comment: Optional[str] = None) -> Path:
        key_path = self.key_dir / name
        if key_path.exists():
            raise FileExistsError(f"Key already exists: {key_path}")

        comment = comment or (
            f"{os.getenv('USER', 'user')}@{os.uname().nodename}"
            f"-{datetime.now():%Y-%m-%d}"
        )
        cmd = ["ssh-keygen", "-t", key_type, "-f", str(key_path),
               "-N", passphrase, "-C", comment]
        if key_type == "ed25519":
            cmd += ["-a", "100"]
        subprocess.run(cmd, check=True, capture_output=True)
        key_path.chmod(0o600)
        key_path.with_suffix(".pub").chmod(0o644)
        return key_path

    def get_key_info(self, pub_key_path: Path) -> SSHKeyInfo:
        out = subprocess.run(
            ["ssh-keygen", "-lf", str(pub_key_path)],
            capture_output=True, text=True, check=True,
        ).stdout.strip().split()
        return SSHKeyInfo(
            key_type=out[-1].strip("()"),   # (ED25519) -> ED25519
            bits=int(out[0]),
            fingerprint=out[1],
            comment=" ".join(out[2:-1]),
            file_path=str(pub_key_path),
        )

    def list_all_keys(self) -> list[SSHKeyInfo]:
        keys = []
        for pub_file in self.key_dir.glob("*.pub"):
            try:
                keys.append(self.get_key_info(pub_file))
            except subprocess.CalledProcessError:
                continue
        return keys

    def audit_weak_keys(self) -> list[SSHKeyInfo]:
        weak = []
        for key in self.list_all_keys():
            if key.key_type in ("DSA", "ECDSA"):
                weak.append(key)
            elif key.key_type == "RSA" and key.bits < 4096:
                weak.append(key)
        return weak


if __name__ == "__main__":
    manager = SSHKeyManager()
    for k in manager.list_all_keys():
        print(f"{k.file_path}: {k.key_type} {k.bits} {k.fingerprint} ({k.comment})")

    for k in manager.audit_weak_keys():
        print(f"WEAK: {k.file_path} ({k.key_type} {k.bits})")
