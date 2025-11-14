import socket
from collections import defaultdict
import threading 
from request import Request
from response import Response
from router.router import Router

class Server:
    def __init__(self, bind_ip="0.0.0.0", bind_port = 9999):
        self.__bind_ip = bind_ip
        self.__bind_port = bind_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clients = defaultdict(list)
        self.__router = Router(routes={"/" : "index.html"})
        self.__setup()


    def __setup(self):
        self.socket.bind((self.bind_ip, self.bind_port))
        self.socket.listen(5)
        self.socket.settimeout(1.0)  # 1-second timeout to check for KeyboardInterrupt

    @property
    def socket(self): return self.__socket
    @property
    def bind_ip(self): return self.__bind_ip
    @property
    def bind_port(self): return self.__bind_port
    @property
    def router(self): return self.__router
    @property
    def clients(self): return self.__clients


    def handle_client(self, client_socket: socket.socket, addr):
        data = client_socket.recv(1024)
        request = Request(data) 
        self.clients[addr[0]].append(request)
        print(f"[+] {request.method} {request.path}")
        if not self.router.route_exists(request.path):
            #TODO redirect to notfound page here???
            print(f"[!] Route {request.path} does not exist.")
        else:
            response = Response(request)
            response.body = self.router.route_to_html(request.path)
            client_socket.send(response.encode())

        
        client_socket.close()

    def run(self):
        print(f"[*] Server started on port {self.bind_port}")

        try:
            while True:
                try:
                    client, addr = self.socket.accept()
                    client_handler = threading.Thread(target=self.handle_client, args=(client, addr))
                    client_handler.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\n[!] Shutting down socket...")
        finally:
            self.socket.close()
            print("[*] Server closed.")