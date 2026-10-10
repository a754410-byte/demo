import hashlib

# Listing 2-4: feed the message to the hasher one byte at a time
hasher = hashlib.md5()
for part in (b"a", b"l", b"i", b"c", b"e"):
    hasher.update(part)

print("Incremental:", hasher.hexdigest())
print("One-shot:   ", hashlib.md5(b"alice").hexdigest())
