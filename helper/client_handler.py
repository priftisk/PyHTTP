from collections import defaultdict
import socket
from pyhttp.request.request import Request

request_repr = lambda x: f"{x.method} {x.path} {x.timestamp}"


class ClientHandler:
    def __init__(self):
        self.__clients = defaultdict(list)

    @property
    def clients(self):
        return self.__clients

    @clients.setter
    def clients(self, value):
        self.__clients = value

    def add_client(self, addr: socket.socket, request: Request):
        self.clients[addr].append(request_repr(request))
