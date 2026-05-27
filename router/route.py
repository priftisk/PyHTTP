class Route:
    def __init__(self, path: str, handler: function):
        if not path or not handler:
            raise Exception("Path and handler keys are mandatory when defining routes.")

        self.__path = path
        self.__handler = handler

    @property
    def path(self):
        return self.__path

    @property
    def handler(self):
        return self.__handler

    @path.setter
    def path(self, value):
        self.__path = value

    @handler.setter
    def handler(self, value):
        self.__handler = value
