import socket
from collections import defaultdict
import threading 
from request import Request
from response import Response


class Server:
    def __init__(self, bind_ip="0.0.0.0", bind_port = 9999):
        self.__bind_ip = bind_ip
        self.__bind_port = bind_port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clients = defaultdict(list)
        self.__setup()


    def __setup(self):
        self.server.bind((self.bind_ip, self.bind_port))
        self.server.listen(5)
        self.server.settimeout(1.0)  # 1-second timeout to check for KeyboardInterrupt

    @property
    def server(self): return self.__server
    @property
    def bind_ip(self): return self.__bind_ip
    @property
    def bind_port(self): return self.__bind_port

    @property
    def clients(self): return self.__clients


    def handle_client(self, client_socket, addr):
        data = client_socket.recv(1024)
        request = Request(data) 
        self.clients[addr[0]].append(request)
        print(f"[+] {request.method} {request.path}")
        response = Response(request)
        client_socket.send(response.encode())
        client_socket.close()

    def run(self):
        print(f"[*] Server started on port {self.bind_port}")

        try:
            while True:
                try:
                    client, addr = self.server.accept()
                    client_handler = threading.Thread(target=self.handle_client, args=(client, addr))
                    client_handler.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\n[!] Shutting down server...")
        finally:
            self.server.close()
            print("[*] Server closed.")