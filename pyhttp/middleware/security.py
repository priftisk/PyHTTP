from pyhttp.request.request import Request
from pyhttp.middleware.middleware import Middleware
from pyhttp.logger.logger import Logger


class AllowedHosts(Middleware):
    def __init__(self, logger: Logger | None = None):
        super().__init__(name="Allowed Hosts", logger=logger)
        try:
            from settings import ALLOWED_HOSTS

            self.__allowed_hosts = ALLOWED_HOSTS
        except ImportError:
            self.__allowed_hosts = []
            if self.logger:
                self.logger.error(
                    "ALLOWED_HOSTS not found — all hosts will be blocked."
                )

    def handle(self, request: Request) -> tuple[bool, str | None]:
        host = request.headers.host.split(":")[0]
        if host not in self.__allowed_hosts:
            self.error_msg = f"Host: {request.headers.host} is not allowed."
            if self.logger:
                self.logger.error(self.error_msg)
            return False, self.error_msg
        return self.call_next(request)
