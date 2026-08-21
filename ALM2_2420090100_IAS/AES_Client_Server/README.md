# AES Client-Server File Transfer using PyCryptodome

This project implements AES encryption in a client-server architecture using Python sockets and the PyCryptodome package.

## Requirements covered

1. Client sends a human-readable **10 KB text file** to the server.
2. Client displays the original plain text and AES cipher text before sending.
3. Server receives the cipher text, decrypts it, and displays both cipher text and recovered plain text.
4. Server sends a different human-readable **5 KB text file** to the client.
5. Server displays the original plain text and cipher text before sending.
6. Client receives the cipher text, decrypts it, and displays both cipher text and recovered plain text.
7. Screenshots are included in the `screenshots/` folder.

## AES details

- Library: PyCryptodome
- Algorithm: AES-128
- Mode: CBC
- Key size: 16 bytes / 128 bits
- IV: Random 16-byte IV generated for every encryption
- Cipher representation: Base64 for readable terminal display
- Transport: TCP socket on `127.0.0.1:5000`

> The hard-coded key is used only to keep this college lab demonstration easy to run. Real applications should never hard-code encryption keys in source code.

## Project structure

```text
AES_Client_Server/
├── aes_utils.py
├── client.py
├── server.py
├── requirements.txt
├── README.md
├── data/
│   ├── client_10kb.txt
│   └── server_5kb.txt
└── screenshots/
    ├── 01_server_started.png
    ├── 02_client_send_10kb.png
    ├── 03_server_received_10kb.png
    ├── 04_server_send_5kb.png
    └── 05_client_received_5kb.png
```

## How to run in VS Code

Open the `AES_Client_Server` folder in VS Code. Then open a terminal and run:

```bash
pip install -r requirements.txt
```

Open **Terminal 1** and run:

```bash
python server.py
```

Open **Terminal 2** and run:

```bash
python client.py
```

The client first sends the encrypted 10 KB file. The server decrypts it and then sends its own encrypted 5 KB file back to the client.

## GitHub submission

Upload the whole folder to GitHub, including the `screenshots` directory.
