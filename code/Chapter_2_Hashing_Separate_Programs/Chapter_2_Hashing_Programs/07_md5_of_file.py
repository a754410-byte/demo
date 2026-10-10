import hashlib
import sys

def md5_of_file(path, block_size=65536):
    hasher = hashlib.md5()
    with open(path, "rb") as file:
        while True:
            block = file.read(block_size)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 07_md5_of_file.py <file_path>")
        raise SystemExit(1)
    print(md5_of_file(sys.argv[1]))
