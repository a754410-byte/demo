# Extracted from: Chapter-3 Symmetric Encryption Tutorial.pdf
# Listing 3-4: AES Exercise Example
# NOTE: The PDF marks this as a partial listing / requires surrounding code.
# Partial Listing: Some Assembly Required

ifile, ofile = sys.argv[1:3]
with open(ifile, "rb") as reader:
  with open(ofile, "wb+") as writer:
    image_data = reader.read()
    header, body = image_data[:54], image_data[54:]
    body += b"\x00"*(16-(len(body)%16))
    writer.write(header + aesEncryptor.update(body))
