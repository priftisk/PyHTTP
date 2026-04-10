class Config:
    def __init__(self, host="0.0.0.0", port=9999):
        self.__host = host
        self.__port = port

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @host.setter
    def host(self, value):
        self.__host = value

    @port.setter
    def port(self, value):
        self.__port = value

    def parse(self):
        try:
            import settings as config

            self.host = config.SERVER_HOST
            self.port = config.SERVER_PORT
        except ImportError as e:
            raise Exception(e.msg)
