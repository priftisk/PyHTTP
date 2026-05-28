class Config:
    def __init__(self, host="0.0.0.0", port=9999):
        self.__host = host
        self.__port = port
        self.__middlewares: list[str] = []
        self.parse()

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

    @property
    def middlewares(self):
        return self.__middlewares

    @middlewares.setter
    def middlewares(self, value):
        self.__middlewares = value

    def parse(self):
        try:
            import settings as config

            self.host = config.SERVER_HOST
            self.port = config.SERVER_PORT
            self.middlewares = config.MIDDLEWARE
        except ImportError as e:
            raise Exception(e.msg)
