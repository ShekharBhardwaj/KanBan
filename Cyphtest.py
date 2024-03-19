from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import binascii

# Function to hash your key to the correct length
def hash_key(your_string):
    hasher = SHA256.new(your_string.encode())  # Hashing the string with SHA256
    return hasher.digest()  # Returns a 32 byte key

# Encrypt function
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)  # New cipher object for encryption
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    hex_ciphertext = binascii.hexlify(ciphertext).decode()
    nonce = cipher.nonce
    return hex_ciphertext, nonce, tag

# Decrypt function
def decrypt_message(hex_ciphertext, nonce, key):
    ciphertext = binascii.unhexlify(hex_ciphertext.encode())
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)  # New cipher object for decryption
    decrypted_message = cipher.decrypt(ciphertext).decode()
    return decrypted_message

# Your string to be used as a key and your message
your_string = "your_password_here"
message = "Hello, world!"

# Hash your string to a 32 byte key
key = hash_key(your_string)

# Encrypt your message
hex_ciphertext, nonce, tag = encrypt_message(message, key)
print(f"Hex Encrypted: {hex_ciphertext}")

# Decrypt your message
decrypted_message = decrypt_message(hex_ciphertext, nonce, key)
print(f"Decrypted Message: {decrypted_message}")
