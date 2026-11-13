"""Version-tagged key rotation — the signature itself carries which key
produced it ("v2:<hex>"), so verification picks the right secret without
trying every key in the ring."""
import hmac
import hashlib
import time


class KeyRotator:
    """Rotates HMAC secrets; signatures carry their key version."""

    def __init__(self):
        self.keys: dict[str, dict] = {}
        self.active_version: str | None = None

    def add_key(self, version: str, secret: str, activate: bool = True):
        self.keys[version] = {"secret": secret, "created": time.time()}
        if activate:
            self.active_version = version

    def retire_key(self, version: str):
        self.keys.pop(version, None)
        if self.active_version == version:
            # Fall back to the most recently added key
            self.active_version = max(
                self.keys, key=lambda v: self.keys[v]["created"], default=None
            )

    def sign(self, method: str, path: str, body: str, timestamp: str) -> str:
        if not self.active_version:
            raise RuntimeError("No active signing key")
        secret = self.keys[self.active_version]["secret"]
        message = f"{method.upper()}{path}{timestamp}{body}"
        sig = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
        return f"{self.active_version}:{sig}"

    def verify(self, method: str, path: str, body: str, timestamp: str, signature: str) -> bool:
        version, _, received = signature.partition(":")
        info = self.keys.get(version)
        if not received or not info:
            return False
        message = f"{method.upper()}{path}{timestamp}{body}"
        expected = hmac.new(info["secret"].encode(), message.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(received, expected)


if __name__ == "__main__":
    rot = KeyRotator()
    rot.add_key("v1", "secret-v1")
    ts = "1730000000"
    sig_v1 = rot.sign("POST", "/api/orders", "{}", ts)
    rot.add_key("v2", "secret-v2")          # rotate: v2 becomes active
    sig_v2 = rot.sign("POST", "/api/orders", "{}", ts)
    print(sig_v1, "->", rot.verify("POST", "/api/orders", "{}", ts, sig_v1))  # still valid
    print(sig_v2, "->", rot.verify("POST", "/api/orders", "{}", ts, sig_v2))
    rot.retire_key("v1")
    print("v1 after retire:", rot.verify("POST", "/api/orders", "{}", ts, sig_v1))  # False
