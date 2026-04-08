from pyfingerprint.pyfingerprint import PyFingerprint
import time
from feature_reduce import reduce_features

try:
    f = PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError('Wrong sensor password')

    print("✅ Sensor connected")
    print("Place your finger...")

    # Wait for finger
    while not f.readImage():
        pass

    print("✅ Image captured")

    # Convert image to characteristics in buffer 1
    f.convertImage(0x01)

    # Download characteristics
    characteristics = f.downloadCharacteristics(0x01)

    print("✅ Characteristics length:", len(characteristics))

    # Reduce fingerprint features
    reduced_vector = reduce_features(characteristics)

    print("✅ Reduced vector (hex):")
    print(reduced_vector.hex())

except Exception as e:
    print("Error:", e)