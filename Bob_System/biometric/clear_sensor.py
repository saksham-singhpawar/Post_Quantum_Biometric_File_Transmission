from pyfingerprint.pyfingerprint import PyFingerprint

try:
    f = PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError('Wrong sensor password')

    print("Sensor connected")

    print("Templates before deletion:", f.getTemplateCount())

    # Delete all templates
    if f.clearDatabase():
        print("All fingerprint templates deleted successfully!")

    print("Templates after deletion:", f.getTemplateCount())

except Exception as e:
    print("Operation failed!")
    print("Error:", e)