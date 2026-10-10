# Extracted from: AES - Modes_ECB_CBC_CTR Tutorial.pdf
# padding_demo.py - PKCS#7 padding for AES (block size = 16 bytes)
from cryptography.hazmat.primitives import padding

BLOCK = 16  # AES block size in bytes (128 bits)


def pkcs7_pad(data: bytes, block: int = BLOCK) -> bytes:
    pad_len = block - (len(data) % block)      # always 1..16, never 0
    return data + bytes([pad_len]) * pad_len   # every pad byte stores pad_len


def pkcs7_unpad(padded: bytes, block: int = BLOCK) -> bytes:
    if len(padded) == 0 or len(padded) % block != 0:
        raise ValueError("padded data length is not a multiple of the block size")
    pad_len = padded[-1]                       # last byte tells how many to strip
    if pad_len < 1 or pad_len > block:
        raise ValueError("invalid padding length byte")
    if padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("padding bytes are corrupt")
    return padded[:-pad_len]


def show_blocks(data: bytes) -> None:
    for i in range(0, len(data), BLOCK):
        print(f"    block {i // BLOCK}: {data[i:i + BLOCK].hex(' ')}")


print("=== 1. PKCS#7 padding for different message lengths ===")
for msg in [b"HELLO", b"ATTACK AT DAWN!!", b"ATTACK AT DAWN!! OK"]:
    padded = pkcs7_pad(msg)
    print(f"message={msg!r} len={len(msg)} -> padded len={len(padded)}, "
          f"pad bytes={len(padded) - len(msg)}")
    show_blocks(padded)

print("\n=== 2. Unpadding restores the original message ===")
padded = pkcs7_pad(b"HELLO")
print("padded  :", padded)
print("unpadded:", pkcs7_unpad(padded))

print("\n=== 3. Manual padding equals the library padder ===")
padder = padding.PKCS7(128).padder()           # 128 = block size in BITS
lib_padded = padder.update(b"HELLO") + padder.finalize()
print("identical to manual version:", lib_padded == pkcs7_pad(b"HELLO"))

print("\n=== 4. Why zero padding is ambiguous ===")
original = b"DATA\x00"                         # genuine trailing zero byte
zero_padded = original + b"\x00" * (BLOCK - len(original) % BLOCK)
recovered = zero_padded.rstrip(b"\x00")        # receiver strips every zero
print("original :", original)
print("recovered:", recovered)
print("data lost:", recovered != original)

print("\n=== 5. Corrupt padding is detected ===")
bad = padded[:-1] + b"\x07"                    # last byte no longer matches
try:
    pkcs7_unpad(bad)
except ValueError as err:
    print("ValueError:", err)
