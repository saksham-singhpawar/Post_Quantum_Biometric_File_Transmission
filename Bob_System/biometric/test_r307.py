from pyfingerprint.pyfingerprint import PyFingerprint
import time

try:
    f = PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError('Wrong sensor password')

    print("Sensor connected!")
    print("Place your finger to enroll...")

    while not f.readImage():
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()

    positionNumber = result[0]

    if positionNumber >= 0:
        print("Fingerprint already exists at position:", positionNumber)
    else:
        print("Remove finger...")
        time.sleep(2)

        print("Place the same finger again...")

        while not f.readImage():
            pass

        f.convertImage(0x02)

        if f.compareCharacteristics() == 0:
            raise Exception("Fingers do not match")

        f.createTemplate()

        positionNumber = f.storeTemplate()

        print("Fingerprint enrolled at position:", positionNumber)

except Exception as e:
    print("Error:", e)