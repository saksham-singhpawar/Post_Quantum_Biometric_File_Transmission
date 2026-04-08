import hashlib

def generate_keypair(seed):

    # Deterministic private key
    private_key = hashlib.shake_256(seed).digest(32)

    # Public key derived from private key
    public_key = hashlib.sha256(private_key).digest()

    return public_key, private_key