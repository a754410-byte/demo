# Extracted from: AES - Modes_ECB_CBC_CTR Tutorial.pdf
# compare_modes.py - ECB vs CBC vs CTR on the same input
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
IV = bytes.fromhex("a0a1a2a3a4a5a6a7a8a9aaabacadaeaf")
NONCE_BLOCK = bytes.fromhex("f0f1f2f3f4f5f6f7") + bytes(8)


def pad(data):
    p = padding.PKCS7(128).padder()
    return p.update(data) + p.finalize()


def run(mode, data):
    op = Cipher(algorithms.AES(KEY), mode).encryptor()
    return op.update(data) + op.finalize()


def unique_blocks(ct):
    return len({ct[i:i + 16] for i in range(0, len(ct), 16)})


msg = b"ABCDEFGHIJKLMNOP" * 4 + b"tail"       # 4 identical blocks + 4 bytes
results = {
    "ECB": run(modes.ECB(), pad(msg)),
    "CBC": run(modes.CBC(IV), pad(msg)),
    "CTR": run(modes.CTR(NONCE_BLOCK), msg),
}
print(f"plaintext length = {len(msg)} bytes, identical 16-byte blocks = 4")
print(f"{'Mode':<5}{'CT length':>10}{'Padding bytes':>15}{'Unique CT blocks':>18}")
for name, ct in results.items():
    extra = len(ct) - len(msg) if name != "CTR" else 0
    print(f"{name:<5}{len(ct):>10}{extra:>15}{unique_blocks(ct):>18}")
