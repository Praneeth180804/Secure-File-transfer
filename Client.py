import socket
from cryptography.fernet import Fernet
import os

if not os.path.exists("secret.key"):
    print("[!] secret.key not found. Generate it using key_gen.py")
    exit()

with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(('127.0.0.1', 5000))
except ConnectionRefusedError:
    print("[!] Cannot connect to server. Start server.py first.")
    exit()

file_path = "client.txt"

if not os.path.exists(file_path):
    print(f"[!] File '{file_path}' not found.")
    exit()

with open(file_path, "rb") as f:
    while True:
        chunk = f.read(4096)
        if not chunk:
            break
        encrypted_chunk = fernet.encrypt(chunk)
        client_socket.send(encrypted_chunk)

print("[+] File sent successfully.")
client_socket.close()
