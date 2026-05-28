from pyhttp.request.request import Request
from pyhttp.response.response_headers import ResponseHeaders
from pyhttp.response.response_body import ResponseBody

mappings: dict[int, str] = {
    200: "OK",
    201: "Created",
    401: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}


class Response:
    def __init__(
        self, request: Request, status_code: int = 200, content_type: str = "html"
    ):
        self.__request: Request = request
        self.__http_version: str = "HTTP/1.1"
        self.__status_code: int = status_code
        self.__status_message: str = mappings[self.status_code] or "OK"
        self.__headers: ResponseHeaders = ResponseHeaders(content_type=content_type)
        self.__body: ResponseBody = ResponseBody()

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

    def __response(self, header_str: str, body_bytes: bytes):
        return (
            f"{self.__http_version} {self.__status_code} {self.__status_message}\r\n"
            f"{header_str}\r\n\r\n"
        ).encode("utf-8") + body_bytes

    def encode(self):
        body_bytes = self.body.encode("utf-8")

        header_str = self.headers.encode(body_bytes)

        return self.__response(header_str, body_bytes)
