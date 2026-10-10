# Extracted from: AES - Modes_ECB_CBC_CTR Tutorial.pdf
# cbc_demo.py - AES in CBC mode
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
IV1 = bytes.fromhex("a0a1a2a3a4a5a6a7a8a9aaabacadaeaf")   # demo IV only
IV2 = bytes.fromhex("b0b1b2b3b4b5b6b7b8b9babbbcbdbebf")   # a different IV


def cbc_encrypt(key, iv, plaintext):
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()
    enc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return enc.update(padded) + enc.finalize()


def cbc_decrypt(key, iv, ciphertext):
    dec = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    padded = dec.update(ciphertext) + dec.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


def blocks(data):
    return [data[i:i + 16] for i in range(0, len(data), 16)]


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


print("=== 1. Round trip and the role of the IV ===")
pt = b"SAMEBLOCK_16BYTE" * 3 + b"DIFFERENT_BLOCK!"
ct1 = cbc_encrypt(KEY, IV1, pt)
ct2 = cbc_encrypt(KEY, IV2, pt)
for i, c in enumerate(blocks(ct1)):
    print(f"IV1 block {i}: {c.hex()}")
print("same plaintext, different IV -> different ciphertext:", ct1 != ct2)
print("repeated blocks now equal? :", blocks(ct1)[0] == blocks(ct1)[1])
print("decrypted OK:", cbc_decrypt(KEY, IV1, ct1) == pt)

print("\n=== 2. Rebuilding CBC by hand: C[i] = E(P[i] xor C[i-1]) ===")
raw = Cipher(algorithms.AES(KEY), modes.ECB()).encryptor()   # bare block cipher
padder = padding.PKCS7(128).padder()
padded = padder.update(pt) + padder.finalize()
prev, manual = IV1, b""
for p in blocks(padded):
    c = raw.update(xor(p, prev))      # XOR with previous ciphertext, then AES
    manual += c
    prev = c                          # chain: this ciphertext feeds the next block
print("manual chain equals library:", manual == ct1)

print("\n=== 3. Bit-flipping: damage caused by editing ciphertext ===")
msg = b"PAY TO: ALICE   " + b"AMOUNT: $ 100   "
ct = cbc_encrypt(KEY, IV1, msg)
tampered = bytearray(ct)
tampered[10] ^= ord("1") ^ ord("9")        # edit byte 10 of C0
res = cbc_decrypt(KEY, IV1, bytes(tampered))
print("P0 (garbled):", res[:16])
print("P1 (chosen) :", res[16:32])

print("\n=== 4. Wrong IV only damages the first block ===")
res = cbc_decrypt(KEY, IV2, ct1)
print("P0 correct?", res[:16] == pt[:16], "| P1..P3 correct?", res[16:] == pt[16:])
