import hashlib

def bits(digest_bytes):
    return "".join(format(byte, "08b") for byte in digest_bytes)

def avalanche(a, b):
    ha = bits(hashlib.md5(a).digest())
    hb = bits(hashlib.md5(b).digest())
    differing = sum(x != y for x, y in zip(ha, hb))
    print(f"{a!r} vs {b!r}")
    print(f" {differing} of {len(ha)} bits differ ({100 * differing / len(ha):.1f}%)")

if __name__ == "__main__":
    avalanche(b"alice", b"balice")
    avalanche(b"alice", b"alicf")
