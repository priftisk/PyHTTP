from middleware.middleware import Middleware
from request.request import Request


class AllowedHosts(Middleware):
    def __init__(self, hosts=[]):
        self.__allowed_hosts = hosts
        self.__error_msg = None
        super().__init__("Allowed Hosts")

    @property
    def error_msg(self):
        return self.__error_msg

    @error_msg.setter
    def error_msg(self, value):
        self.__error_msg = value

    def verify(self, request: Request):
        super().verify(request)
        if not request.headers.host.split(":")[0] in self.__allowed_hosts:
            self.error_msg = f"Host: {request.headers.host} is not allowed."
            return False
        return True
