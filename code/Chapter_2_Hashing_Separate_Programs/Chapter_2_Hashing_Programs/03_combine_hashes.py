import hashlib

# Listing 2-3: construct, hash and display in one expression
print("alice:", hashlib.md5(b"alice").hexdigest())
print("bob:  ", hashlib.md5(b"bob").hexdigest())
