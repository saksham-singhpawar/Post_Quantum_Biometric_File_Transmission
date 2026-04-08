import socket
from authenticate import authenticate_and_generate_keys

HOST = '0.0.0.0'
PORT = 5000

def start_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print("✅ Waiting for Alice to register public key...")

        conn, addr = s.accept()

        with conn:
            print("✅ Connected by", addr)

            keys = authenticate_and_generate_keys()

            if not keys:
                print("❌ Authentication failed.")
                return

            public_key, private_key, user_id, master_secret = keys

            conn.sendall(public_key)

            print(f"✅ Public key sent for user: {user_id}")
            print("✅ Private key deleted from memory.")

            del private_key

if __name__ == "__main__":
    start_server()