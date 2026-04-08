from pyfingerprint.pyfingerprint import PyFingerprint
import secrets
import time
from database.db import init_db, insert_or_replace_user
from pqc.keygen import generate_keypair
from authenticate import derive_seed

def enroll_user():

    init_db()

    user_id = input("Enter User ID for enrollment: ").strip()

    f = PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError("Sensor password incorrect")

    print("Place finger to enroll...")

    while not f.readImage():
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber >= 0:
        print("Fingerprint already enrolled.")
        return

    print("Remove finger...")
    time.sleep(2)

    print("Place same finger again...")

    while not f.readImage():
        pass

    f.convertImage(0x02)

    if f.compareCharacteristics() == 0:
        raise Exception("Fingerprints do not match")

    f.createTemplate()
    positionNumber = f.storeTemplate()

    print("✅ Fingerprint enrolled successfully.")

    # Generate master secret
    master_secret = secrets.token_bytes(32)

    # Derive seed
    seed = derive_seed(master_secret, positionNumber)

    # Generate keypair (for public key export)
    public_key, private_key = generate_keypair(seed)

    # Store user in database
    insert_or_replace_user(user_id, positionNumber, master_secret)

    print("✅ Public key generated.")
    print("✅ Private key deleted from memory.")

    del private_key

    return public_key


if __name__ == "__main__":
    enroll_user()