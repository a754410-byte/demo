import hashlib

# Listing 2-6: same input, different hash algorithms
data = b"alice"
for algorithm in ("md5", "sha1", "sha256"):
    digest = hashlib.new(algorithm, data).hexdigest()
    print(f"{algorithm.upper():6} {len(digest):2} hex characters  {digest}")
