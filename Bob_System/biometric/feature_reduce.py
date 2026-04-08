import hashlib

def reduce_features(characteristics):

    # Convert to bytes
    char_bytes = bytes(characteristics)

    block_size = len(char_bytes) // 32
    reduced = b''

    for i in range(32):
        block = char_bytes[i*block_size:(i+1)*block_size]
        block_hash = hashlib.sha256(block).digest()
        reduced += block_hash[:1]  # take first byte

    return reduced  # 32 bytes