import json
import socket
import struct
from pathlib import Path
from aes_utils import encrypt_bytes, decrypt_bytes

HOST = "127.0.0.1"
PORT = 5000
CLIENT_FILE = Path("data/client_10kb.txt")

def send_packet(sock, obj):
    data = json.dumps(obj).encode("utf-8")
    sock.sendall(struct.pack("!I", len(data)) + data)

def recv_exact(sock, n):
    chunks = []
    remaining = n
    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError("Connection closed unexpectedly")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)

def recv_packet(sock):
    size = struct.unpack("!I", recv_exact(sock, 4))[0]
    return json.loads(recv_exact(sock, size).decode("utf-8"))

def main():
    print("=== AES CLIENT STARTED ===\n")
    client_plain = CLIENT_FILE.read_text(encoding="utf-8")
    encrypted = encrypt_bytes(client_plain.encode("utf-8"))

    print("--- SENDING TO SERVER (10 KB) ---")
    print("Plain Text:")
    print(client_plain)
    print("\nCipher Text (Base64):")
    print(encrypted["ciphertext"])
    print(f"\nSending plaintext bytes: {len(client_plain.encode('utf-8'))}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        send_packet(sock, encrypted)

        packet = recv_packet(sock)
        server_plain = decrypt_bytes(packet["iv"], packet["ciphertext"]).decode("utf-8")
        print("\n--- RECEIVED FROM SERVER (5 KB) ---")
        print("Cipher Text (Base64):")
        print(packet["ciphertext"])
        print("\nDecrypted Plain Text:")
        print(server_plain)
        print(f"\nReceived plaintext bytes: {len(server_plain.encode('utf-8'))}")

    print("\n=== CLIENT FINISHED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
