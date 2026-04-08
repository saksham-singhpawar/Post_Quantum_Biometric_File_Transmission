import hashlib
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from authenticate import authenticate_and_generate_keys


def embed_watermark(text, user_id, master_secret):

    start_watermark = time.perf_counter()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Integrity signature
    signature = hashlib.sha256(
        (user_id + "|" + master_secret.hex()).encode()
    ).hexdigest()

    payload = user_id + "|" + timestamp + "|" + signature

    # Convert to binary
    binary_string = ''.join(format(ord(c), '08b') for c in payload)

    # Zero-width encoding
    zero_width = ''.join('\u200B' if bit == '0' else '\u200C'
                         for bit in binary_string)

    watermarked_text = text + "\n" + zero_width

    end_watermark = time.perf_counter()
    watermark_time = end_watermark - start_watermark

    print(f"✅ Watermark embedding time: {watermark_time:.6f} seconds")

    return watermarked_text


def decrypt_and_watermark():

    print("=== Secure Decryption (Bob) ===")

    try:
        with open("received_package.bin", "rb") as f:
            package = f.read()
    except:
        print("❌ No encrypted package found.")
        return

    print("✅ Encrypted package loaded.")

    enc_key_length = int.from_bytes(package[:4], 'big')
    encapsulated_key = package[4:4 + enc_key_length]
    nonce = package[4 + enc_key_length:4 + enc_key_length + 12]
    ciphertext = package[4 + enc_key_length + 12:]

    print("✅ Package parsed.")

    # Authenticate
    start_auth = time.perf_counter()
    keys = authenticate_and_generate_keys()
    end_auth = time.perf_counter()

    if not keys:
        print("❌ Authentication failed.")
        return

    auth_time = end_auth - start_auth
    print(f"✅ Fingerprint authentication time: {auth_time:.6f} seconds")

    public_key, private_key, user_id, master_secret = keys

    # Decrypt
    start_decrypt = time.perf_counter()

    aes_key = bytes([a ^ b for a, b in zip(encapsulated_key, public_key[:32])])
    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    end_decrypt = time.perf_counter()
    decrypt_time = end_decrypt - start_decrypt

    print(f"✅ AES decryption time: {decrypt_time:.6f} seconds")

    text = plaintext.decode()

    # Embed watermark
    watermarked_text = embed_watermark(text, user_id, master_secret)

    # ✅ SAVE FILE
    with open("decrypted_watermarked.txt", "w", encoding="utf-8") as f:
        f.write(watermarked_text)

    print("✅ File decrypted and saved as decrypted_watermarked.txt")

    del private_key
    print("✅ Private key deleted from memory.")


if __name__ == "__main__":
    decrypt_and_watermark()