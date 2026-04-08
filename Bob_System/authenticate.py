from pyfingerprint.pyfingerprint import PyFingerprint
from database.db import get_user_by_position
from pqc.keygen import generate_keypair
import hashlib


def derive_seed(master_secret, template_position):
    """
    Derive deterministic seed from master_secret and template_position.
    """
    position_bytes = template_position.to_bytes(4, 'big')
    seed = hashlib.sha256(master_secret + position_bytes).digest()
    return seed


def authenticate_and_generate_keys():
    """
    1. Ask for fingerprint
    2. Match template inside R307
    3. Retrieve user_id and master_secret from DB
    4. Derive seed
    5. Generate keypair
    6. Return public_key, private_key, user_id
    """

    try:
        # Initialize fingerprint sensor
        f = PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError("Sensor password incorrect")

        print("Place finger for authentication...")

        # Wait for finger
        while not f.readImage():
            pass

        f.convertImage(0x01)

        # Search template inside sensor
        result = f.searchTemplate()
        positionNumber = result[0]

        if positionNumber < 0:
            print("❌ Fingerprint not recognized.")
            return None

        # Fetch user record from database
        user_data = get_user_by_position(positionNumber)

        if user_data is None:
            print("❌ No user record found.")
            return None

        user_id, master_secret = user_data

        # Derive seed
        seed = derive_seed(master_secret, positionNumber)

        # Generate deterministic keypair
        public_key, private_key = generate_keypair(seed)

        print("✅ Authentication successful.")
        print("✅ Private key generated in RAM.")

        # Return everything needed
        return public_key, private_key, user_id, master_secret

    except Exception as e:
        print("Authentication Error:", e)
        return None