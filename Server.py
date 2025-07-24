import socket
from cryptography.fernet import Fernet
import os

if not os.path.exists("secret.key"):
    print("[!] secret.key not found. Generate it using key_gen.py")
    exit()

with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000))
server_socket.listen(1)

print("[+] Listening on 0.0.0.0:5000 ... Waiting for connection")
conn, addr = server_socket.accept()
print(f"[+] Connection established with {addr}")

with open("received_file.txt", "wb") as f:
    while True:
        data = conn.recv(4096)
        if not data:
            break
        decrypted_data = fernet.decrypt(data)
        f.write(decrypted_data)

print("[+] File received and saved as received_file.txt")
conn.close()
server_socket.close()
