import binascii
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

# Function to convert hex string to bytes for key
def hex_string_to_bytes(hex_string):
    return binascii.unhexlify(hex_string)

# Your hex string
my_hex_string = "your_hex_string_here"  # Replace with your actual hex string

# Convert your hex string to a byte string (derived key)
derived_key = hex_string_to_bytes(my_hex_string)

# Example usage with encryption and decryption functions
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    hex_ciphertext = binascii.hexlify(ciphertext).decode()
    nonce = cipher.nonce
    return hex_ciphertext, nonce, tag

def decrypt_message(hex_ciphertext, nonce, key):
    ciphertext = binascii.unhexlify(hex_ciphertext.encode())
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_message = cipher.decrypt(ciphertext).decode()
    return decrypted_message

# Hash a string to use as a key if you don't have a hex string ready
# your_string = "some_password_or_secret"
# key = SHA256.new(your_string.encode()).digest()

# For demonstration, using the derived_key directly
message = "Hello, world!"

# Encrypt your message
hex_ciphertext, nonce, tag = encrypt_message(message, derived_key)
print(f"Hex Encrypted: {hex_ciphertext}")

# Decrypt your message
decrypted_message = decrypt_message(hex_ciphertext, nonce, derived_key)
print(f"Decrypted Message: {decrypted_message}")
