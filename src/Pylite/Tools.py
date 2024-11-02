from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
from base64 import b64encode, b64decode

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def print_warning(text):
    print(f"{bcolors.WARNING}{text}{bcolors.ENDC}")

def derive_key(password: str, salt: bytes) -> bytes:
    """Generate a secure key from a password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt(data: bytes, password: str) -> bytes:
    """
    Encrypt binary data using AES-GCM.
    
    Args:
        data: Binary data to encrypt
        password: Password for encryption
    
    Returns:
        Encrypted binary data with salt, IV, and tag
    """
    salt = os.urandom(16)  # Generate a random salt
    iv = os.urandom(12)    # Generate a random IV (nonce)
    key = derive_key(password, salt)
    
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()
    
    # No need to encode data since it's already in bytes
    ciphertext = encryptor.update(data) + encryptor.finalize()
    
    # Combine all components into a single bytes object
    return salt + iv + encryptor.tag + ciphertext

def decrypt(encrypted_data: bytes, password: str) -> bytes:
    """
    Decrypt binary data using AES-GCM.
    
    Args:
        encrypted_data: Encrypted binary data containing salt, IV, tag, and ciphertext
        password: Password for decryption
    
    Returns:
        Decrypted binary data
    """
    salt = encrypted_data[:16]      # Extract the salt
    iv = encrypted_data[16:28]      # Extract the IV (nonce)
    tag = encrypted_data[28:44]     # Extract the GCM tag
    ciphertext = encrypted_data[44:] # Extract the encrypted data
    
    key = derive_key(password, salt)
    
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    
    # Return the decrypted bytes directly
    return decryptor.update(ciphertext) + decryptor.finalize()