import socket
from collections import defaultdict
import threading 
from request import Request
from response import Response


bind_ip = "0.0.0.0" 
bind_port = 9999

clients = defaultdict(list)

def handle_client(client_socket, addr):
    data = client_socket.recv(1024)
    request = Request(data) 
    clients[addr[0]].append(request)
    print(f"[+] {request.method} {request.path}")
    response = Response(request)
    client_socket.send(response.encode())
    client_socket.close()

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", bind_port))
    server.listen(5)
    server.settimeout(1.0)  # 1-second timeout lets us check for KeyboardInterrupt
    print(f"[*] Server started on port {bind_port}")

    try:
        while True:
            try:
                client, addr = server.accept()
                client_handler = threading.Thread(target=handle_client, args=(client, addr))
                client_handler.start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\n[!] Shutting down server...")
    finally:
        server.close()
        print("[*] Server closed.")

if __name__ == "__main__":
    run_server()    