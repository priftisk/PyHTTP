class ResponseBody:
    def __init__(
        self,
        raw_data="",
    ):
        self.__raw_data: str = raw_data

    def encode(self, encoding: str = "utf"):
        return self.__raw_data.encode(encoding)
