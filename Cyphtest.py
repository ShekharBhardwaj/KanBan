from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import binascii

# Your string to be used as a key
your_string = "your_password_here"

# Hash the string to ensure it's 32 bytes long
hasher = SHA256.new(your_string.encode())
key = hasher.digest()

# Create cipher object
cipher = AES.new(key, AES.MODE_EAX)

# Your message
message = "Hello, world!"

# Encrypt the message
ciphertext, tag = cipher.encrypt_and_digest(message.encode())

# Convert ciphertext to hex string for storage or transmission
hex_ciphertext = binascii.hexlify(ciphertext).decode()

print(f"Hex Encrypted: {hex_ciphertext}")

# Function to decrypt the message
def decrypt_message(hex_ciphertext, key):
    ciphertext = binascii.unhexlify(hex_ciphertext.encode())

    # Create a new cipher object using the same key and mode
    cipher = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)

    # Decrypt the message
    decrypted_message = cipher.decrypt(ciphertext).decode()

    return decrypted_message

# Decrypt the message
decrypted_message = decrypt_message(hex_ciphertext, key)
print(f"Decrypted Message: {decrypted_message}")
