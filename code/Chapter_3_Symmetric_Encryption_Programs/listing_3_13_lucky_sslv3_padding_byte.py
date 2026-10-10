# Extracted from: Chapter-3 Symmetric Encryption Tutorial.pdf
# Listing 3-13: Lucky SSLv3 Padding Byte
# NOTE: The PDF marks this as a partial listing / requires surrounding code.
# Partial Listing: Some Assembly Required

# This function assumes that the last ciphertext block is a full
# block of SSLV3 padding
def lucky_get_one_byte(iv, ciphertext, block_number, oracle):
  block_start = block_number * 16
  block_end = block_start + 16
  block = ciphertext[block_start: block_end]

  # Copy the block over the last block.
  mod_ciphertext = ciphertext[:-16] + block
  if not oracle.accept(mod_ciphertext):
    return False, None

  # This is valid! Let's get the byte!
  # We first need the byte decrypted from the block.
  # It was XORed with second to last block, so
  # byte = 15 XOR (last byte of second-to-last block).
  second_to_last = ciphertext[-32:-16]
  intermediate = second_to_last[-1]^15

  # We still have to XOR it with its *real*
  # preceding block in order to get the true value.
  if block_number == 0:
    prev_block = iv
  else:
    prev_block = ciphertext[block_start-16: block_start]

  return True, intermediate ^ prev_block[-1]
