from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import binascii

# Function to simulate Node.js Buffer.from() behavior for hexadecimal string to bytes
def buffer_from_hex_string(hex_string):
    return binascii.unhexlify(hex_string)

# Assuming you have the key as a hex string after some process, similar to Node.js derived key
# If you're directly using a buffer (array of bytes) as shown in your IV, you can directly assign it
# Example: aes_key = bytes([your_key_bytes_here])

# For this example, I'm directly using the IV you've provided as the example key is not given
aes_key = bytes([0])  # Example, adjust as needed for the key

# Ensure key is of correct length for AES-256
if len(aes_key) != 32:
    raise ValueError("Key must be 32 bytes (256 bits) for AES-256.")

# Your provided IV for AES-256-CBC
iv = bytes([0])

cipher = AES.new(aes_key, AES.MODE_CBC, iv)

# Encrypt a message
message = "Hello, world!"
ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))

# Base64 encode the ciphertext for output
encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')

print("Encoded Ciphertext (Base64):", encoded_ciphertext)

# Decrypt the message for demonstration
cipher_dec = AES.new(aes_key, AES.MODE_CBC, iv)
plaintext = unpad(cipher_dec.decrypt(base64.b64decode(encoded_ciphertext)), AES.block_size).decode('utf-8')

print("Decrypted Message:", plaintext)
