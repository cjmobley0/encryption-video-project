"""The real cryptographic output shown on screen.

The professional cut is for a technical audience, so nothing here is invented:
every hex string the viewer reads is the actual output of the named algorithm
on the named input. They are computed at import, so a value cannot drift from
its caption — change the message and the screen changes with it.

``cryptography`` is only needed for the AES line. If it is missing the baked
literal is used instead, which is the same string this file produces; the
SHA-256 values need nothing but the standard library either way.

    .venv/bin/python values.py     # print everything, to check against the plan

The AES key here is ``00 01 02 ... 1f`` with an all-zero nonce. That is a demo
key, chosen so the value is reproducible by anyone reading the plan. Never
reuse a fixed key and nonce for anything real: with AES-GCM, one repeated
nonce under one key is enough to break the encryption.
"""

from __future__ import annotations

import base64
import hashlib

# The message every scene encrypts, hashes and signs. One string, so Scene 2's
# ciphertext and Scene 10's hash are visibly of the same plaintext.
MSG = "Meet at 3pm"
MSG_TAMPERED = "Meet at 4pm"

DEMO_KEY = bytes(range(32))   # AES-256: 32 bytes
DEMO_NONCE = bytes(12)        # GCM: 96-bit nonce

# AES-256-GCM over MSG: 11 bytes of ciphertext followed by the 16-byte tag.
_AES_HEX_BAKED = "43d9d0aa954df79d3bd8c4ab98d9cbed4ffddc6e1aae9365dbb646"

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    AES_HEX = AESGCM(DEMO_KEY).encrypt(DEMO_NONCE, MSG.encode(), None).hex()
except ImportError:  # pragma: no cover - the baked value is the same string
    AES_HEX = _AES_HEX_BAKED

assert AES_HEX == _AES_HEX_BAKED, (
    "AES output moved away from the value printed in the plan — update both"
)

# Scene 2 re-renders the same bytes as Base64, to show that the encoding is a
# presentation choice and the ciphertext underneath has not changed.
AES_B64 = base64.b64encode(bytes.fromhex(AES_HEX)).decode()

# Scene 10: the avalanche. One character of the message changes and almost
# every character of the digest changes with it.
SHA_MSG = hashlib.sha256(MSG.encode()).hexdigest()
SHA_TAMPERED = hashlib.sha256(MSG_TAMPERED.encode()).hexdigest()

# Scene 10 again: a two-character input and a long one hash to the same width,
# which is the point of "fixed-length".
SHA_SHORT = hashlib.sha256(b"hi").hexdigest()
LONG_INPUT = (
    "Encryption is the process of transforming readable information into an "
    "unreadable format so that unauthorized people cannot understand it."
)
SHA_LONG = hashlib.sha256(LONG_INPUT.encode()).hexdigest()

# Scene 10: a salted password row, the way a real table stores one.
PASSWORD = "hunter2"
SALT = "7f3a1c08"
SHA_PASSWORD = hashlib.sha256((SALT + PASSWORD).encode()).hexdigest()


def diff_positions(a: str = SHA_MSG, b: str = SHA_TAMPERED) -> list[int]:
    """Which characters of two digests differ — the avalanche highlight."""
    return [i for i in range(min(len(a), len(b))) if a[i] != b[i]]


def wrap(text: str, width: int = 32) -> str:
    """Split a hex string into fixed-width lines for the screen."""
    return "\n".join(text[i:i + width] for i in range(0, len(text), width))


if __name__ == "__main__":
    pairs = [
        ("MSG", MSG),
        ("AES-256-GCM", AES_HEX),
        ("  as Base64", AES_B64),
        (f"SHA-256({MSG!r})", SHA_MSG),
        (f"SHA-256({MSG_TAMPERED!r})", SHA_TAMPERED),
        ("SHA-256('hi')", SHA_SHORT),
        ("SHA-256(long input)", SHA_LONG),
        (f"SHA-256(salt + {PASSWORD!r})", SHA_PASSWORD),
    ]
    for name, value in pairs:
        print(f"{name:32} {value}")
    changed = len(diff_positions())
    print(f"{'avalanche':32} {changed}/{len(SHA_MSG)} hex characters differ")
