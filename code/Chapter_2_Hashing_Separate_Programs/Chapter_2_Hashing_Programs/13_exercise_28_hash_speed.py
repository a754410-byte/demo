"""Compare digest computation speeds for Exercise 2.8.
This is a timing demonstration, not a password-cracking tool.
"""
import hashlib
import time

DATA = b"classroom-demo-password"
REPEATS = 200_000

if __name__ == "__main__":
    for algorithm in ("md5", "sha1", "sha256"):
        start = time.perf_counter()
        for _ in range(REPEATS):
            hashlib.new(algorithm, DATA).digest()
        elapsed = time.perf_counter() - start
        print(f"{algorithm.upper():6}: {REPEATS:,} hashes in {elapsed:.3f} seconds")
    print("The PDF also asks students to try scrypt; see 09_scrypt_password.py.")
