from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA1
import base64

# Your passphrase or secret key
passphrase = "your_secret_passphrase_here"

# Your message
message = "Hello, world!"

# Parameters from your Node.js setup
iterations = 123456
key_length = 32  # for AES-256
digest = SHA1
algorithm = 'AES-256-CBC'
init_vector = bytes([0])
input_encoding = 'utf-8'
output_encoding = 'base64'

# Deriving key using PBKDF2
salt = b''  # If you're using salt, it needs to be the same as in Node.js; it can be empty or specific bytes
key = PBKDF2(passphrase, salt, dkLen=key_length, count=iterations, hmac_hash_module=SHA1)

# Encrypting the message
cipher = AES.new(key, AES.MODE_CBC, init_vector)
ciphertext = cipher.encrypt(pad(message.encode(input_encoding), AES.block_size))

# Encoding the ciphertext in base64 to match the Node.js output
encoded_ciphertext = base64.b64encode(ciphertext).decode(output_encoding)

print(f"Encoded Ciphertext: {encoded_ciphertext}")
