import socket

HOST = '0.0.0.0'
PORT = 6000

def start_receiver():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        print("✅ Waiting for encrypted file...")

        conn, addr = s.accept()

        with conn:
            print("✅ Connected by", addr)

            size_data = conn.recv(8)
            file_size = int.from_bytes(size_data, 'big')

            received = b''
            while len(received) < file_size:
                packet = conn.recv(4096)
                received += packet

    with open("received_package.bin", "wb") as f:
        f.write(received)

    print("✅ Encrypted package saved as received_package.bin")

if __name__ == "__main__":
    start_receiver()