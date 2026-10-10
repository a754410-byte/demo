# Extracted from: Chapter-3 Symmetric Encryption Tutorial.pdf
# Listing 3-12: SSLv3 Padding Oracle
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class Oracle:
  def __init__(self, key, iv):
    self.key = key
    self.iv = iv

  def accept(self, ciphertext):
    aesCipher = Cipher(algorithms.AES(self.key),
              modes.CBC(self.iv),
              backend=default_backend())
    decryptor = aesCipher.decryptor()
    plaintext = decryptor.update(ciphertext)
    plaintext += decryptor.finalize()
    return plaintext[-1] == 15
