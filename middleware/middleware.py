from abc import ABC, abstractmethod
from request.request import Request
from logger.logger import Logger


class Middleware(ABC):
    def __init__(self, name: str, logger: Logger | None = None):
        self.__name = name
        self.__error_msg = "Default middleware error message."
        self.__next: Middleware | None = None
        self.__logger = logger

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def error_msg(self) -> str:
        return self.__error_msg

    @error_msg.setter
    def error_msg(self, value: str):
        self.__error_msg = value

    @property
    def logger(self):
        return self.__logger

    def set_next(self, middleware: Middleware) -> Middleware:
        self.__next = middleware
        return middleware

    def call_next(self, request: Request) -> tuple[bool, str | None]:
        if self.__next:
            return self.__next.handle(request)
        return True, None

    @abstractmethod
    def handle(self, request: Request) -> tuple[bool, str | None]:
        pass
