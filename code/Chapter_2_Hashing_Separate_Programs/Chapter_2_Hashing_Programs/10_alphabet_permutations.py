def generate(alphabet, max_len):
    """Yield every string of length 1 through max_len, without building a list."""
    if max_len <= 0:
        return
    for char in alphabet:
        yield char
    for char in alphabet:
        for suffix in generate(alphabet, max_len - 1):
            yield char + suffix

if __name__ == "__main__":
    alphabet = input("Enter a small alphabet (e.g. ab): ")
    max_len = int(input("Maximum string length: "))
    print(list(generate(alphabet, max_len)))
