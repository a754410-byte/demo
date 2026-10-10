import hashlib

# Exercise 2.1: compare MD5 digests for the inputs listed in the tutorial
samples = [
    ("b'alice'", b"alice"),
    ("b'bob'", b"bob"),
    ("b'balice'", b"balice"),
    ("b'cob'", b"cob"),
    ("b'a'", b"a"),
    ("b'aa'", b"aa"),
    ("b'aaaaaaaaaa'", b"a" * 10),
    ("b'a' * 100000", b"a" * 100000),
]

for label, data in samples:
    print(f"{label:20} {hashlib.md5(data).hexdigest()}")
