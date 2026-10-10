# Extracted from: AES - Modes_ECB_CBC_CTR Tutorial.pdf
# ecb_demo.py - AES in ECB mode (educational use only - ECB is NOT secure)
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")   # 128-bit demo key


def ecb_encrypt(key: bytes, plaintext: bytes) -> bytes:
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()      # step 1: pad
    enc = Cipher(algorithms.AES(key), modes.ECB()).encryptor() # step 2: ECB
    return enc.update(padded) + enc.finalize()


def ecb_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    dec = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    padded = dec.update(ciphertext) + dec.finalize()           # step 1: decrypt
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()       # step 2: unpad


def blocks(data: bytes):
    return [data[i:i + 16] for i in range(0, len(data), 16)]


print("=== 1. Encrypt / decrypt round trip ===")
message = b"Meet me at the library at 9 PM."
ct = ecb_encrypt(KEY, message)
print("plaintext :", message, f"({len(message)} bytes)")
print("ciphertext:", ct.hex(), f"({len(ct)} bytes)")
print("decrypted :", ecb_decrypt(KEY, ct))

print("\n=== 2. Identical plaintext blocks -> identical ciphertext blocks ===")
pt = b"SAMEBLOCK_16BYTE" * 3 + b"DIFFERENT_BLOCK!"
ct = ecb_encrypt(KEY, pt)
for i, (p, c) in enumerate(zip(blocks(pt), blocks(ct))):
    print(f"block {i}: P={p.decode()}  C={c.hex()}")
print("C0 == C1 == C2 :", blocks(ct)[0] == blocks(ct)[1] == blocks(ct)[2])

print("\n=== 3. Block reordering goes undetected ===")
order = b"PAY TO: ALICE   " + b"AMOUNT: $ 100   " + b"SIGNED: BANK-1  "
ct_blocks = blocks(ecb_encrypt(KEY, order))
swapped = [ct_blocks[2], ct_blocks[1], ct_blocks[0], ct_blocks[3]]  # attacker
print("original :", ecb_decrypt(KEY, b"".join(ct_blocks)))
print("tampered :", ecb_decrypt(KEY, b"".join(swapped)))
