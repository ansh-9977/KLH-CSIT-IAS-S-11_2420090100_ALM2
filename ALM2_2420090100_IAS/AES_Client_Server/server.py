import json
import socket
import struct
from pathlib import Path
from aes_utils import encrypt_bytes, decrypt_bytes

HOST = "127.0.0.1"
PORT = 5000
SERVER_FILE = Path("data/server_5kb.txt")

def send_packet(conn, obj):
    data = json.dumps(obj).encode("utf-8")
    conn.sendall(struct.pack("!I", len(data)) + data)

def recv_exact(conn, n):
    chunks = []
    remaining = n
    while remaining:
        chunk = conn.recv(remaining)
        if not chunk:
            raise ConnectionError("Connection closed unexpectedly")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)

def recv_packet(conn):
    size = struct.unpack("!I", recv_exact(conn, 4))[0]
    return json.loads(recv_exact(conn, size).decode("utf-8"))

def main():
    print("=== AES SERVER STARTED ===")
    print(f"Listening on {HOST}:{PORT}\n")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        with conn:
            print(f"Client connected from {addr}\n")

            # 1. Receive encrypted 10 KB file from client
            packet = recv_packet(conn)
            plaintext = decrypt_bytes(packet["iv"], packet["ciphertext"]).decode("utf-8")
            print("--- RECEIVED FROM CLIENT (10 KB) ---")
            print("Cipher Text (Base64):")
            print(packet["ciphertext"])
            print("\nDecrypted Plain Text:")
            print(plaintext)
            print(f"\nReceived plaintext bytes: {len(plaintext.encode('utf-8'))}")

            # 2. Encrypt and send a different 5 KB file to client
            server_plain = SERVER_FILE.read_text(encoding="utf-8")
            encrypted = encrypt_bytes(server_plain.encode("utf-8"))
            print("\n--- SENDING TO CLIENT (5 KB) ---")
            print("Plain Text:")
            print(server_plain)
            print("\nCipher Text (Base64):")
            print(encrypted["ciphertext"])
            print(f"\nSending plaintext bytes: {len(server_plain.encode('utf-8'))}")
            send_packet(conn, encrypted)

    print("\n=== SERVER FINISHED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
