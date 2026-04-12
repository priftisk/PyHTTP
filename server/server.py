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
        self.__logger = Logger()
        self.__config = config
        self.__middlewares = self.__load_middlewares()

    def __load_middlewares(self) -> Middleware | None:
        middlewares = []
        for m in self.__config.middlewares:
            module_path, class_name = m.rsplit(".", 1)
            module = importlib.import_module(module_path)
            middleware = getattr(module, class_name)
            middlewares.append(middleware(logger=self.__logger))

        for i in range(len(middlewares) - 1):
            middlewares[i].set_next(middlewares[i + 1])

        return middlewares[0] if middlewares else None

    def __verify_middlewares(self, request: Request) -> tuple[bool, str | None]:
        if not self.__middlewares:
            return True, None
        return self.__middlewares.handle(request)

    def handle_client(self, client_socket: socket.socket, addr):
        data = client_socket.recv(1024)
        request = Request(data)

        if not request.valid:
            self.__logger.error("Invalid request. Closing connection...")
            return client_socket.close()

        self.__client_handler.add_client(addr, request)

        try:
            valid, _ = self.__verify_middlewares(request)

            if not valid:
                response = Response(request, 401)
            elif not self.__router.route_exists(request.path):
                self.__logger.error(f"Route {request.path} does not exist.")
                response = Response(request, 404)
            else:
                response = Response(request)
                response.body = self.__router.path_to_html(request.path)

            client_socket.send(response.encode())
        finally:
            self.__logger.info(
                f"{request.method} {request.path} {response.status_code}"
            )
            client_socket.close()

    def run(self):
        self.__logger.info(
            f"Server started {self.__socket.bind_ip}:{self.__socket.bind_port}"
        )
        try:
            while True:
                try:
                    client, addr = self.__socket.socket.accept()
                    threading.Thread(
                        target=self.handle_client, args=(client, addr)
                    ).start()
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            self.__logger.info("Shutting down socket...")
        finally:
            self.__socket.socket.close()
            self.__logger.info("Server closed.")
