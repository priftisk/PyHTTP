import socket, threading
from request.request import Request
from response.response import Response
from router.router import Router
from helper.client_handler import ClientHandler
from middleware.middleware import Middleware
from logger.logger import Logger
from config.config import Config
from .server_socket import ServerSocket
import importlib


class Server:
    def __init__(self, config: Config):
        self.__socket = ServerSocket(config)
        self.__router = Router()
        self.__client_handler = ClientHandler()
        self.__middlewares: list[Middleware] = []
        self.__logger: Logger = Logger()
        self.__config: Config = config
        self.__setup()

    def __setup_middlewares(self):
        for m in self.config.middlewares:
            parts = m.rsplit(".", 1)
            module = importlib.import_module(parts[0])
            class_name = getattr(module, parts[1])
            self.__middlewares.append(class_name())

    def __setup_from_config(self):
        self.__setup_middlewares()

    def __setup(self):
        self.__setup_from_config()

    @property
    def config(self):
        return self.__config

    @property
    def client_handler(self):
        return self.__client_handler

    @property
    def socket(self):
        return self.__socket

    @property
    def router(self):
        return self.__router

    @property
    def clients(self):
        return self.__clients

    @property
    def logger(self):
        return self.__logger

    def verify_middlewares(self, request: Request) -> bool | str:
        for m in self.__middlewares:
            if not m.verify(request):
                return False, m.error_msg
        return True, None

    def handle_client(self, client_socket: socket.socket, addr):
        data = client_socket.recv(1024)
        request = Request(data)
        if not request.valid:
            self.logger.error("Invalid request. Closing connection...")
            return client_socket.close()
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
                html_body = self.router.path_to_html(request.path)
                response = Response(request)
                response.body = html_body

            self.send_response(client_socket, response)

        finally:
            self.logger.info(f"{request.method} {request.path} {response.status_code}")
            client_socket.close()

    def send_response(self, client_socket, response):
        client_socket.send(response.encode())

    def run(self):
        self.logger.info(
            f"Server started {self.socket.bind_ip}:{self.socket.bind_port}"
        )

        try:
            while True:
                try:
                    client, addr = self.socket.socket.accept()
                    client_handler = threading.Thread(
                        target=self.handle_client, args=(client, addr)
                    )
                    client_handler.start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            self.logger.info("Shutting down socket...")
        finally:
            self.socket.socket.close()
            self.logger.info("Server closed.")
