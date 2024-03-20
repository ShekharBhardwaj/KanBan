from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

# Function to simulate Node.js Buffer.from() behavior for hexadecimal string to bytes
def buffer_from_hex_string(hex_string):
    return binascii.unhexlify(hex_string)

# Example hex string that represents your derived key
hex_string_key = "your_hex_key_here"  # Replace this with your actual hex key

# Convert hex string to bytes to use as an AES key
aes_key = buffer_from_hex_string(hex_string_key)

# Assuming AES-256-CBC, the key should be 32 bytes long
if len(aes_key) != 32:
    raise ValueError("Key must be 32 bytes (256 bits) for AES-256-CBC.")

# Initialize AES cipher with CBC mode
# Note: You'll need an IV for AES-CBC; for demonstration, we'll generate a simple one.
# In practice, IV should be random and unique for each encryption but doesn't need to be secret.
iv = bytes([0]*16)  # Example static IV for demonstration; replace with a proper IV in real use

cipher = AES.new(aes_key, AES.MODE_CBC, iv)

# Encrypt a message
message = "Hello, world!"
ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))

# Decrypt the message
cipher_dec = AES.new(aes_key, AES.MODE_CBC, iv)
plaintext = unpad(cipher_dec.decrypt(ciphertext), AES.block_size).decode('utf-8')

print("Ciphertext (Hex):", binascii.hexlify(ciphertext).decode())
print("Decrypted Message:", plaintext)
