from cryptography.fernet import Fernet
import os

# Generate a key and instantiate a Fernet instance
def load_key():
    key_file = 'key.key'
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(key_file, 'rb') as key_file:
            key = key_file.read()
    return Fernet(key)

# Encrypt a message
def encrypt_message(message, fernet_instance):
    return fernet_instance.encrypt(message.encode())

# Decrypt a message
def decrypt_message(encrypted_message, fernet_instance):
    return fernet_instance.decrypt(encrypted_message).decode()
