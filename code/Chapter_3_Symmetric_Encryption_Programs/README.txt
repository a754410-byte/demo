CHAPTER 3 — SYMMETRIC ENCRYPTION PROGRAMS
===========================================

The ZIP contains separate Python files extracted from both uploaded PDFs.

AES Modes of Operation tutorial:
  padding_demo.py
  ecb_demo.py
  ecb_image_demo.py
  cbc_demo.py
  ctr_demo.py
  compare_modes.py
  random_iv_demo.py

Chapter 3 Symmetric Encryption tutorial:
  listing_3_01_...py through listing_3_13_...py (separate files per listing)

Install dependencies:
  python -m pip install cryptography numpy matplotlib

Run a program:
  python filename.py

Important:
- Some Chapter 3 examples are deliberately insecure educational demonstrations.
- Listing 3-4 and Listing 3-13 are partial examples in the source material.
- Do not use ECB or reuse CBC IVs / CTR nonces in real applications.
- This archive is extracted from the PDFs; check the original listing if a snippet
  appears incomplete. Prefer authenticated encryption such as AES-GCM in production.
