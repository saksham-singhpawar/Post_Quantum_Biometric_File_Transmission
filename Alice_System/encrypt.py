from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_file(data, public_key):

    # Generate random AES-256 key
    aes_key = os.urandom(32)

    # AES-GCM encryption
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    # Simulated Kyber encapsulation
    encapsulated_key = bytes([a ^ b for a, b in zip(aes_key, public_key[:32])])

    return encapsulated_key, nonce, ciphertext