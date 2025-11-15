import socket
import threading
from request.request import Request
from response.response import Response
from router.router import Router
from client_handler import ClientHandler


class Server:
    def __init__(self, bind_ip="0.0.0.0", bind_port=9999):
        self.__bind_ip = bind_ip
        self.__bind_port = bind_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__router = Router(routes={"/": "index.html"})
        self.__client_handler = ClientHandler()
        self.__setup()

    def __setup(self):
        self.socket.bind((self.bind_ip, self.bind_port))
        self.socket.listen(5)
        self.socket.settimeout(1.0)  # 1-second timeout to check for KeyboardInterrupt

    @property
    def client_handler(self):
        return self.__client_handler

    @property
    def socket(self):
        return self.__socket

    @property
    def bind_ip(self):
        return self.__bind_ip

    @property
    def bind_port(self):
        return self.__bind_port

    @property
    def router(self):
        return self.__router

    @property
    def clients(self):
        return self.__clients

    def handle_client(self, client_socket: socket.socket, addr):
        data = client_socket.recv(1024)
        request = Request(data)
        self.client_handler.add_client(addr, request)
        print(
            f"[+] {request.method} {request.path} [{request.timestamp.today().strftime("%d/%m/%Y %H:%M:%S")}]"
        )
        if not self.router.route_exists(request.path):
            response = Response(request, 404)
            print(f"[!] Route {request.path} does not exist.")
        else:
            response = Response(request)
            html_body = self.router.route_to_html(request.path)
            response.body = html_body

        client_socket.send(response.encode())
        client_socket.close()

    def run(self):
        print(f"[*] Server started {self.bind_ip}:{self.bind_port}")

        try:
            while True:
                try:
                    client, addr = self.socket.accept()
                    client_handler = threading.Thread(
                        target=self.handle_client, args=(client, addr)
                    )
                    client_handler.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\n[!] Shutting down socket...")
        finally:
            self.socket.close()
            print("[*] Server closed.")
