class ResponseHeaders:

    def __init__(self, content_type):
        self.__content_type = self.__set_content_type(content_type)
        self.__content_length = 0
        self.__connection = "Keep-Alive"

    @property
    def content_length(self):
        return self.__content_length

    @content_length.setter
    def content_length(self, value):
        self.__content_length = value

    @property
    def content_type(self):
        return self.__content_type

    @property
    def connection(self):
        return self.__connection

    @content_type.setter
    def content_type(self, value):
        self.__content_type = value

    def __set_content_type(self, ct):
        h = "text/html; charset=utf-8"
        if ct == "json":
            h = "application/json"
        return h

    def encode(self, body_bytes: bytes):
        self.content_length = str(len(body_bytes))
        return "\r\n".join(
            f"{k}: {v}"
            for k, v in {
                "Content-Type": self.content_type,
                "Connection": self.connection,
                "Content-Length": self.content_length,
            }.items()
        )
