from router.router import Router
from request import Request
class Response:
    def __init__(self, request):
        self.__request: Request = request
        self.__router = Router(routes={"/" : "index.html"})
        self.__http_version = "HTTP/1.1"
        self.__status_code = 200
        self.__status_message = "OK"
        self.__headers = {
            "Content-Type": "text/html; charset=utf-8"
        }
        self.__body = "<html><body><h1>The default page</h1></body></html>"

    @property
    def router(self): return self.__router

    @property
    def request(self): return self.__request

    def encode(self):
        # Compute content length
        html = self.router.route_to_html(self.request.path)
        self.__body = html
        body_bytes = self.__body.encode("utf-8")
        self.__headers["Content-Length"] = str(len(body_bytes))
        # Build the header section
        header_str = "\r\n".join(f"{k}: {v}" for k, v in self.__headers.items())

        response = (
            f"{self.__http_version} {self.__status_code} {self.__status_message}\r\n"
            f"{header_str}\r\n\r\n"
        ).encode("utf-8") + body_bytes

        return response
