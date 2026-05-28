import socket
from pyhttp.config.config import Config


class ServerSocket:
    def __init__(self, config: Config):
        self.__bind_ip = None
        self.__bind_port = None
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__setup(config)

    def __setup(self, config: Config):
        self.__bind_ip = config.host
        self.__bind_port = config.port
        self.socket.bind((self.bind_ip, self.bind_port))
        self.socket.listen(5)
        self.socket.settimeout(1.0)  # 1-second timeout to check for KeyboardInterrupt

    @property
    def bind_ip(self):
        return self.__bind_ip

    @bind_ip.setter
    def bind_ip(self, value):
        self.__bind_ip = value

    @property
    def bind_port(self):
        return self.__bind_port

    @bind_port.setter
    def bind_port(self, value):
        self.__bind_port = value

    @property
    def socket(self):
        return self.__socket
