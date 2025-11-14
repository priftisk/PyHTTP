from request import Request

mappings = {200: "OK", 404: "Not Found"}

class Response:
    def __init__(self, request, status_code = 200):
        self.__request: Request = request
        self.__http_version = "HTTP/1.1"
        self.__status_code = status_code
        self.__status_message = "OK"
        self.__headers = {
            "Content-Type": "text/html; charset=utf-8"
        }
        self.__body = "<html><body><h1>Not found.</h1></body></html>"

    @property
    def status_code(self): return self.__status_code

        
    @property
    def status_message(self): return self.__status_message

    
    @property
    def request(self): return self.__request

    @property
    def body(self): return self.__body

    
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
        self.__headers["Content-Length"] = str(len(body_bytes))

        # Build the header section
        header_str = "\r\n".join(f"{k}: {v}" for k, v in self.__headers.items())

        response = (
            f"{self.__http_version} {self.__status_code} {self.__status_message}\r\n"
            f"{header_str}\r\n\r\n"
        ).encode("utf-8") + body_bytes

        return response
