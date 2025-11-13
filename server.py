import socket
from collections import defaultdict
import threading 
from server.request import Request
from server.response import Response


bind_ip = "0.0.0.0" 
bind_port = 9999

clients = defaultdict(list)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((bind_ip, bind_port)) 
# a maximum backlog of connections set to 5
server.listen(5) 

print(f"[+] Listening on port {bind_ip} : {bind_port}")                            

def handle_client(client_socket, addr): 
    request = Request(client_socket.recv(1024)) 
    clients[addr[0]].append(request)
    print(f"[+] {request.method} {request.path}")
    response = Response(request)
    client_socket.send(response.encode())
    client_socket.close()

def run_server():
    try:
        while True:
            try:
                client, addr = server.accept()
            except socket.timeout:
                continue  # check again
            client_handler = threading.Thread(target=handle_client, args=(client, addr))
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server...")
        server.close()


if __name__ == "__main__":
    run_server()