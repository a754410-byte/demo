# Extracted from: Chapter-3 Symmetric Encryption Tutorial.pdf
# Listing 3-10: AES-CTR for a Store
# ACME generates a purchase message in their storefront.
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# WARNING! Never do this. Reusing a key/IV is irresponsible!
preshared_key = bytes.fromhex('00112233445566778899AABBCCDDEEFF')
preshared_iv = bytes.fromhex('00000000000000000000000000000000')

purchase_message = b"""
<XML>
 <CreditCardPurchase>
  <Merchant>Acme Inc</Merchant>
  <Buyer>John Smith</Buyer>
  <Date>01/01/2001</Date>
  <Amount>$100.00</Amount>
  <CCNumber>555-555-555-555</CCNumber>
 </CreditCardPurchase>
</XML>
"""

aesContext = Cipher(algorithms.AES(preshared_key),
          modes.CTR(preshared_iv),
          backend=default_backend())
encryptor = aesContext.encryptor()
encrypted_message = encryptor.update(purchase_message)
