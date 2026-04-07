from request.request import Request


class Middleware:
    def __init__(self, name):
        self.__name = name
        self.__error_msg = "Default middleware error message."
        pass

    @property
    def name(self):
        return self.__name

    @name.setter
    def set_name(self, value):
        self.__name = value

    @property
    def error_msg(self):
        return self.__error_msg

    @error_msg.setter
    def set_error_msg(self, value):
        self.__error_msg = value

    def verify(self, r: Request):
        pass
