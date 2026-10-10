import hashlib
import time

def mine(block_data, target):
    nonce = 0
    start = time.time()
    while True:
        candidate = block_data + str(nonce).encode("utf-8")
        digest = hashlib.sha256(candidate).digest()
        value = int.from_bytes(digest, byteorder="big")
        if value < target:
            return nonce, digest.hex(), time.time() - start
        nonce += 1

if __name__ == "__main__":
    data = b"Hello, Blockchain!:"
    for zero_bits in (8, 12, 16, 20):
        target = 2 ** (256 - zero_bits)
        nonce, digest, elapsed = mine(data, target)
        print(f"{zero_bits:2} zero bits -> nonce {nonce:>10} {digest[:24]} ({elapsed:.3f} s)")
