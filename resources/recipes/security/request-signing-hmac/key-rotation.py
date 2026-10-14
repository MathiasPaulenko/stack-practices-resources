"""HMAC key rotation with overlap window.

Both the old and new key verify during the overlap so a rotation
never drops in-flight requests or clients mid-flip.
"""
import hashlib
import hmac
import time
from dataclasses import dataclass


@dataclass
class KeyRotation:
    """Manage HMAC key rotation with overlap period."""

    current_key: str
    previous_key: str | None = None
    rotation_time: float = 0
    overlap_seconds: int = 3600  # 1 hour overlap

    def rotate(self, new_key: str):
        """Rotate to a new key, keeping old key valid during overlap."""
        self.previous_key = self.current_key
        self.current_key = new_key
        self.rotation_time = time.time()

    def get_valid_keys(self) -> list[str]:
        """Return all currently valid keys."""
        keys = [self.current_key]
        if self.previous_key and self.previous_key != self.current_key:
            if time.time() - self.rotation_time < self.overlap_seconds:
                keys.append(self.previous_key)
        return keys

    def verify(
        self, signature: str, method: str, path: str, timestamp: str, body: str
    ) -> bool:
        """Verify against any valid key (supports rotation overlap)."""
        message = f"{method}\n{path}\n{timestamp}\n{body}"
        for key in self.get_valid_keys():
            expected = hmac.new(
                key.encode(), message.encode(), hashlib.sha256
            ).hexdigest()
            if hmac.compare_digest(signature, expected):
                return True
        return False


if __name__ == '__main__':
    rotation = KeyRotation(current_key='secret-v1')
    rotation.rotate('secret-v2')
    # During overlap: both v1 and v2 verify; after 1h: only v2
    print('valid keys now:', rotation.get_valid_keys())
