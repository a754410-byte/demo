# Extracted from: AES - Modes_ECB_CBC_CTR Tutorial.pdf
# ctr_demo.py - AES in CTR mode (a stream cipher built from a block cipher)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
NONCE = bytes.fromhex("f0f1f2f3f4f5f6f7")      # 8-byte nonce (demo value)


def counter_block(nonce: bytes, n: int) -> bytes:
    return nonce + n.to_bytes(8, "big")         # 16 bytes = nonce || counter


def ctr_crypt(key, nonce, data, start=0):
    # Encryption and decryption are the SAME operation in CTR mode
    cipher = Cipher(algorithms.AES(key), modes.CTR(counter_block(nonce, start)))
    op = cipher.encryptor()
    return op.update(data) + op.finalize()


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


print("=== 1. No padding: ciphertext length equals plaintext length ===")
msg = b"Meet me at the library at 9 PM."          # 31 bytes
ct = ctr_crypt(KEY, NONCE, msg)
print("plaintext length :", len(msg))
print("ciphertext length:", len(ct))
print("ciphertext       :", ct.hex())
print("decrypted        :", ctr_crypt(KEY, NONCE, ct))

print("\n=== 2. Rebuilding CTR by hand: C = P xor E(nonce||counter) ===")
raw = Cipher(algorithms.AES(KEY), modes.ECB()).encryptor()
keystream = b"".join(raw.update(counter_block(NONCE, i)) for i in range(2))
print("keystream block 0:", keystream[:16].hex())
print("keystream block 1:", keystream[16:].hex())
print("manual result equals library:", xor(msg, keystream) == ct)

print("\n=== 3. Identical blocks give different ciphertext blocks ===")
pt = b"SAMEBLOCK_16BYTE" * 3
ct3 = ctr_crypt(KEY, NONCE, pt)
print([ct3[i:i + 16].hex()[:12] + "..." for i in range(0, 48, 16)])

print("\n=== 4. Random access: decrypt only block 2 ===")
full = ctr_crypt(KEY, NONCE, pt)
only_b2 = ctr_crypt(KEY, NONCE, full[32:48], start=2)   # jump straight to counter 2
print("block 2 recovered alone:", only_b2)

print("\n=== 5. DANGER: nonce reuse leaks plaintext ===")
p1 = b"ATTACK AT DAWN!!"
p2 = b"RETREAT AT NOON!"
c1 = ctr_crypt(KEY, NONCE, p1)
c2 = ctr_crypt(KEY, NONCE, p2)                           # same key + same nonce
print("C1 xor C2 == P1 xor P2 :", xor(c1, c2) == xor(p1, p2))
print("attacker knows P1 -> P2:", xor(xor(c1, c2), p1))

print("\n=== 6. Malleability: bit-flips pass straight through ===")
c = bytearray(ctr_crypt(KEY, NONCE, b"AMOUNT: $ 100   "))
c[10] ^= ord("1") ^ ord("9")
print("tampered plaintext:", ctr_crypt(KEY, NONCE, bytes(c)))
