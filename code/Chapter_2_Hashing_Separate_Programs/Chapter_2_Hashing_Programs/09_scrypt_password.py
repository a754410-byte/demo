"""Demonstration of scrypt password-key derivation and verification.
Requires: python -m pip install cryptography
"""
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey

def make_kdf(salt):
    return Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

if __name__ == "__main__":
    password = input("Enter a demo password: ").encode("utf-8")
    salt = os.urandom(16)
    key = make_kdf(salt).derive(password)

    print("Salt (save this):", salt.hex())
    print("Derived key:", key.hex())

    proposal = input("Enter password again to verify: ").encode("utf-8")
    try:
        make_kdf(salt).verify(proposal, key)
        print("Success! Password matches.")
    except InvalidKey:
        print("Password does not match.")
