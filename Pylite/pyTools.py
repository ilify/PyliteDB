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
    
    

# Generate a secure key from a password
def derive_key(password, salt) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# AES-GCM encryption function
def encrypt(plaintext, password) -> str:
    salt = os.urandom(16)  # Generate a random salt
    iv = os.urandom(12)  # Generate a random IV (nonce)
    key = derive_key(password, salt)
    
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()
    
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    
    return b64encode(salt + iv + encryptor.tag + ciphertext).decode('utf-8')


# AES-GCM decryption function
def decrypt(ciphertext, password) -> str:
    data = b64decode(ciphertext)
    
    salt = data[:16]  # Extract the salt
    iv = data[16:28]  # Extract the IV (nonce)
    tag = data[28:44]  # Extract the GCM tag
    ciphertext = data[44:]  # Extract the encrypted message
    
    key = derive_key(password, salt)
    
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode('utf-8')
