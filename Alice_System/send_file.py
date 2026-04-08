import socket
import os
import time
from encrypt import encrypt_file

BOB_IP = "10.240.47.212"
PORT = 6000

def send_file():

    print("=== Secure File Sender (Alice) ===")

    file_name = input("Enter file name to encrypt: ").strip()

    if not os.path.exists(file_name):
        print("❌ File does not exist.")
        return

    if not os.path.exists("bob_public.key"):
        print("❌ Bob public key not found.")
        return

    with open("bob_public.key", "rb") as f:
        public_key = f.read()

    print("✅ Bob public key loaded.")

    with open(file_name, "rb") as f:
        data = f.read()

    print("✅ File loaded. Starting encryption...")

    start_encrypt = time.perf_counter()
    encapsulated_key, nonce, ciphertext = encrypt_file(data, public_key)
    end_encrypt = time.perf_counter()

    encryption_time = end_encrypt - start_encrypt

    package = (
        len(encapsulated_key).to_bytes(4, 'big') +
        encapsulated_key +
        nonce +
        ciphertext
    )

    print(f"✅ Encryption completed in {encryption_time:.6f} seconds")

    print("✅ Sending encrypted file...")

    start_send = time.perf_counter()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((BOB_IP, PORT))
        s.sendall(len(package).to_bytes(8, 'big'))
        s.sendall(package)

    end_send = time.perf_counter()

    send_time = end_send - start_send

    print(f"✅ File sent in {send_time:.6f} seconds")
    

if __name__ == "__main__":
    send_file()