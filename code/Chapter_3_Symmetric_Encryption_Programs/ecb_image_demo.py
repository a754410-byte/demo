# Extracted from: AES - Modes_ECB_CBC_CTR Tutorial.pdf
# ecb_image_demo.py - why ECB leaks structure (visual proof)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
IV = bytes.fromhex("a0a1a2a3a4a5a6a7a8a9aaabacadaeaf")
CTR0 = bytes.fromhex("f0f1f2f3f4f5f6f7") + bytes(8)

# 128 x 128 grayscale picture: white background, black ring and diagonal bar
y, x = np.mgrid[0:128, 0:128]
ring = (np.hypot(x - 64, y - 64) < 48) & (np.hypot(x - 64, y - 64) > 30)
bar = abs(x - y) < 6
img = np.full((128, 128), 255, dtype=np.uint8)
img[ring | bar] = 0
raw = img.tobytes()                      # 16384 bytes = 1024 AES blocks (no padding)


def encrypt(mode):
    op = Cipher(algorithms.AES(KEY), mode).encryptor()
    return np.frombuffer(op.update(raw) + op.finalize(), dtype=np.uint8)


panels = [("Original", img),
          ("ECB", encrypt(modes.ECB()).reshape(128, 128)),
          ("CBC", encrypt(modes.CBC(IV)).reshape(128, 128)),
          ("CTR", encrypt(modes.CTR(CTR0)).reshape(128, 128))]

fig, axes = plt.subplots(1, 4, figsize=(12, 3.6), facecolor="white")
for ax, (title, data) in zip(axes, panels):
    ax.imshow(data, cmap="gray", vmin=0, vmax=255)
    ax.set_title(title, fontsize=16, fontweight="bold")
    ax.axis("off")
fig.tight_layout()
fig.savefig("fig_ecb_image.png", dpi=300, facecolor="white")
print("saved fig_ecb_image.png")
