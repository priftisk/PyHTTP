from request import Request
class Response:
    def __init__(self, request):
        self.__request: Request = request
        self.__http_version = "HTTP/1.1"
        self.__status_code = 200
        self.__status_message = "OK"
        self.__headers = {
            "Content-Type": "text/html; charset=utf-8"
        }
        self.__body = "<html><body><h1>Not found.</h1></body></html>"

    @property
    def request(self): return self.__request

    @property
    def body(self): return self.__body

    @body.setter
    def body(self, value):
        self.__body = value

    def encode(self):
        # Compute content length
        body_bytes = self.body.encode("utf-8")
        self.__headers["Content-Length"] = str(len(body_bytes))

        # Build the header section
        header_str = "\r\n".join(f"{k}: {v}" for k, v in self.__headers.items())

        response = (
            f"{self.__http_version} {self.__status_code} {self.__status_message}\r\n"
            f"{header_str}\r\n\r\n"
        ).encode("utf-8") + body_bytes

        return response
