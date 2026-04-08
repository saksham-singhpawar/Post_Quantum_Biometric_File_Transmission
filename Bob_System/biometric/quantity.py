from pyfingerprint.pyfingerprint import PyFingerprint

f = PyFingerprint('COM3', 57600, 0xFFFFFFFF, 0x00000000)

print("Stored templates:", f.getTemplateCount())
print("Sensor capacity:", f.getStorageCapacity())