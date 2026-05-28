from pyhttp.request.request_methods import RequestMethod
from pyhttp.request.request import Request
from .path import Path


class Route:
    def __init__(self, methods: list[RequestMethod], raw_path: str, handler: function):
        self.__methods = methods
        self.__path = Path(raw_path)
        self.__handler = handler

    def invoke_handler(self, *args):
        req: Request = args[0]
        rest = args[1]

        if len(rest) == 0:
            return self.handler(req)
        else:
            params = {k: v for k, v in zip(rest, req.path.parameters)}
            return self.handler(req, params)

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
