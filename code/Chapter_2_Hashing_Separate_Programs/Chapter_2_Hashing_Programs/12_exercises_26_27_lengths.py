"""Small classroom benchmark for Exercises 2.6 and 2.7.
It reports search-space sizes by default. Set MAX_TRIALS low if enabling a real toy search.
"""
import string

ALPHABETS = {
    "lowercase": string.ascii_lowercase,
    "lowercase + uppercase": string.ascii_letters,
    "letters + digits": string.ascii_letters + string.digits,
    "string.printable": string.printable,
}

if __name__ == "__main__":
    print("Alphabet size and total combinations")
    print(f"{'alphabet':24} {'size':>6} {'len 1':>12} {'len 2':>12} {'len 3':>12} {'len 4':>12}")
    for name, alphabet in ALPHABETS.items():
        size = len(alphabet)
        counts = [size ** length for length in range(1, 5)]
        print(f"{name:24} {size:6} " + " ".join(f"{count:12,}" for count in counts))
    print("\nEach extra character multiplies the search space by the alphabet size.")
