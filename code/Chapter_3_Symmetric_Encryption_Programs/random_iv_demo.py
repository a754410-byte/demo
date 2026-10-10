# Extracted from: AES - Modes_ECB_CBC_CTR Tutorial.pdf
# random_iv_demo.py - the production pattern: fresh random IV / nonce every time
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

key = os.urandom(32)                       # random 256-bit AES key
msg = b"Meet me at the library at 9 PM."


def cbc_pack(key, plaintext):
    iv = os.urandom(16)                    # new random IV for EVERY message
    padder = padding.PKCS7(128).padder()
    data = padder.update(plaintext) + padder.finalize()
    enc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return iv + enc.update(data) + enc.finalize()       # ship IV with ciphertext


def cbc_unpack(key, packet):
    iv, body = packet[:16], packet[16:]    # split IV from ciphertext
    dec = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(dec.update(body) + dec.finalize()) + unpadder.finalize()


def ctr_pack(key, plaintext):
    nonce = os.urandom(8)                  # new random 64-bit nonce per message
    enc = Cipher(algorithms.AES(key), modes.CTR(nonce + bytes(8))).encryptor()
    return nonce + enc.update(plaintext) + enc.finalize()


def ctr_unpack(key, packet):
    nonce, body = packet[:8], packet[8:]
    dec = Cipher(algorithms.AES(key), modes.CTR(nonce + bytes(8))).decryptor()
    return dec.update(body) + dec.finalize()


p1, p2 = cbc_pack(key, msg), cbc_pack(key, msg)
print("CBC packet length   :", len(p1), "(16 IV + 32 ciphertext)")
print("two CBC encryptions differ:", p1 != p2)
print("CBC round trip OK   :", cbc_unpack(key, p1) == msg)

q1, q2 = ctr_pack(key, msg), ctr_pack(key, msg)
print("CTR packet length   :", len(q1), "(8 nonce + 31 ciphertext)")
print("two CTR encryptions differ:", q1 != q2)
print("CTR round trip OK   :", ctr_unpack(key, q1) == msg)
