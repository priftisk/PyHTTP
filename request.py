from server.headers import *

class Request:
    def __init__(self, raw_string):
        self.__raw_string: bytes = raw_string
        self.__method = None
        self.__path = None
        self.__http_version = None
        self.__headers = None
        self.parse()
        
        
    @property
    def raw_string(self): return self.__raw_string
    @property
    def method(self): return self.__method
    @property
    def path(self): return self.__path
    @property
    def http_version(self): return self.__http_version
    @property
    def headers(self): return self.__headers
    
    def parse(self):
        decoded = self.raw_string.decode().split("\r\n")[0: -2]
        req = decoded[0].split(" ")
        self.__method = req[0]
        self.__path = req[1]
        self.__http_version = req[2]
        self.__headers = Headers([i.split(":", 1) for i in decoded[1:]])
    