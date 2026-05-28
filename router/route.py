from request.request_methods import RequestMethod


class Route:
    def __init__(self, methods: list[RequestMethod], path: str, handler: function):
        self.__methods = methods
        self.__path = path
        self.__handler = handler

    @property
    def path(self):
        return self.__path

    @property
    def handler(self):
        return self.__handler

    @property
    def methods(self):
        return self.__methods

    @methods.setter
    def methods(self, value):
        self.__methods = value

    @path.setter
    def path(self, value):
        self.__path = value

    @handler.setter
    def handler(self, value):
        self.__handler = value

    def method_allowed(self, method: RequestMethod):
        return method in self.methods
