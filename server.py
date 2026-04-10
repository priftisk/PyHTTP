import socket
import threading
from request.request import Request
from response.response import Response
from router.router import Router
from client_handler import ClientHandler
from middleware.middleware import Middleware
from logger.logger import Logger


class Server:
    def __init__(self, bind_ip="0.0.0.0", bind_port=9999):
        self.__bind_ip = bind_ip
        self.__bind_port = bind_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__router = Router(routes={"/": "index.html"})
        self.__client_handler = ClientHandler()
        self.__middlewares: list[Middleware] = []
        self.__logger: Logger = Logger()
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

    @property
    def logger(self):
        return self.__logger

    def add_middlewares(self, middlewares: list[Middleware]):
        for m in middlewares:
            if m not in self.__middlewares:
                self.__middlewares.append(m)

    def verify_middlewares(self, request: Request) -> bool | str:
        for m in self.__middlewares:
            if not m.verify(request):
                return False, m.error_msg
        return True, None

    def handle_client(self, client_socket: socket.socket, addr):
        data = client_socket.recv(1024)
        request = Request(data)
        self.client_handler.add_client(addr, request)
        try:
            valid, _ = self.verify_middlewares(request)

            if not valid:
                response = Response(request, 401)
                return self.send_response(client_socket, response)

            if not self.router.route_exists(request.path):
                self.logger.error(f"Route {request.path} does not exist.")
                response = Response(request, 404)
            else:
                html_body = self.router.route_to_html(request.path)
                response = Response(request)
                response.body = html_body

            self.send_response(client_socket, response)

        finally:
            self.logger.info(f"{request.method} {request.path} {response.status_code}")
            client_socket.close()

    def send_response(self, client_socket, response):
        client_socket.send(response.encode())

    def run(self):
        self.logger.info(f"Server started {self.bind_ip}:{self.bind_port}")

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
