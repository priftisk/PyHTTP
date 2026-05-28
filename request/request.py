from request.request_headers import *
import datetime
from request.request_path import RequestPath


class Request:
    def __init__(self, raw_string):
        self.__valid = None
        self.__raw_string: bytes = raw_string
        self.__method = None
        self.__path = None
        self.__http_version = None
        self.__headers = None
        self.__timestamp = datetime.datetime.now()
        self.parse()

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def raw_string(self):
        return self.__raw_string

    @property
    def method(self):
        return self.__method

    @property
    def path(self):
        return self.__path

    @property
    def http_version(self):
        return self.__http_version

    @property
    def headers(self):
        return self.__headers

    @property
    def valid(self):
        return self.__valid

    @valid.setter
    def valid(self, value):
        self.__valid = value

    def parse(self):
        self.valid = True
        try:
            decoded = self.raw_string.decode().split("\r\n")[0:-2]
            req = decoded[0].split(" ")
            self.__method = req[0]
            self.__path = RequestPath(req[1])
            self.__http_version = req[2]
            self.__headers = RequestHeaders([i.split(":", 1) for i in decoded[1:]])
        except Exception as e:
            self.valid = False
