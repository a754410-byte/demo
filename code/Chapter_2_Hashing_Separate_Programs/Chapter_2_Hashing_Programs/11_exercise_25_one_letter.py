import hashlib
import random
import string
import time

def crack_one_letter():
    # This program creates its own one-letter test hash.
    secret = random.choice(string.ascii_lowercase)
    target = hashlib.md5(secret.encode("utf-8")).hexdigest()
    start = time.time()

    for candidate in string.ascii_lowercase:
        guess = hashlib.md5(candidate.encode("utf-8")).hexdigest()
        if guess == target:
            return candidate, time.time() - start
    return None, time.time() - start

if __name__ == "__main__":
    total = 0.0
    for trial in range(10):
        found, elapsed = crack_one_letter()
        print(f"trial {trial + 1:2}: found {found!r} in {elapsed:.6f} s")
        total += elapsed
    print(f"average: {total / 10:.6f} s")
