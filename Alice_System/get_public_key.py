import socket

BOB_IP = "10.240.47.212"
PORT = 5000

def get_public_key():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((BOB_IP, PORT))
        public_key = s.recv(4096)

    with open("bob_public.key", "wb") as f:
        f.write(public_key)

    print("✅ Public key stored successfully.")

if __name__ == "__main__":
    get_public_key()