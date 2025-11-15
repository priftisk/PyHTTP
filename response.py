from request import Request
from response_headers import ResponseHeaders

mappings = {200: "OK", 201: "Created", 404: "Not Found", 500: "Internal Server Error"}


class Response:
    def __init__(self, request, status_code=200, content_type="html"):
        self.__request: Request = request
        self.__http_version = "HTTP/1.1"
        self.__status_code = status_code
        self.__status_message = "OK"
        self.__headers = ResponseHeaders(content_type=content_type)
        self.__body = "<html><body><h1>Not found.</h1></body></html>"

    @property
    def status_code(self):
        return self.__status_code

    @property
    def status_message(self):
        return self.__status_message

    @property
    def request(self):
        return self.__request

    @property
    def body(self):
        return self.__body

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value):
        self.__headers = value

    @status_code.setter
    def status_code(self, value):
        self.__status_code = value
        self.status_message = mappings.get(self.status_code, 404)

    @status_message.setter
    def status_message(self, value):
        self.__status_message = value

    @body.setter
    def body(self, value):
        self.__body = value

    def encode(self):
        # Compute content length
        body_bytes = self.body.encode("utf-8")
        self.headers.content_length = str(len(body_bytes))

        # Build the header section
        header_str = self.headers.encode()

        response = (
            f"{self.__http_version} {self.__status_code} {self.__status_message}\r\n"
            f"{header_str}\r\n\r\n"
        ).encode("utf-8") + body_bytes

        return response
