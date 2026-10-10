import hashlib

# Listing 2-2: hash Alice and Bob
for name in (b"alice", b"bob"):
    print(name, hashlib.md5(name).hexdigest())
