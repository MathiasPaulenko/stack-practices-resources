"""RSA-PSS signing and Ed25519 signing — both sides, both algorithms.

Run: pip install cryptography && python rsa-sign-verify.py
"""
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ed25519
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


def rsa_sign(private_key, message: bytes) -> bytes:
    return private_key.sign(
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )


def rsa_verify(public_key, signature: bytes, message: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


def ed_sign(private_key, message: bytes) -> bytes:
    return private_key.sign(message)


def ed_verify(public_key, signature: bytes, message: bytes) -> bool:
    try:
        public_key.verify(signature, message)
        return True
    except InvalidSignature:
        return False


if __name__ == "__main__":
    msg = b"release v2.1.0 checksum:abcd1234"

    rsa_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    sig = rsa_sign(rsa_priv, msg)
    print("rsa-pss  ok:", rsa_verify(rsa_priv.public_key(), sig, msg),
          "| tampered:", rsa_verify(rsa_priv.public_key(), sig, msg + b"!"))

    ed_priv = ed25519.Ed25519PrivateKey.generate()
    sig2 = ed_sign(ed_priv, msg)
    print("ed25519  ok:", ed_verify(ed_priv.public_key(), sig2, msg),
          "| tampered:", ed_verify(ed_priv.public_key(), sig2, msg + b"!"))
