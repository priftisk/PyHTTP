class RequestPath:
    def __init__(self, raw_path: str):
        self.__raw = raw_path
        self.__parameters = []

        if raw_path == "/":  # TODO fix bad solution
            self.__base = "/"
        else:
            parts = list(filter(lambda x: len(x) > 0, raw_path.split("/")))
            if len(parts) == 0:
                raise Exception("Malformed or empty path provided.")
            self.__base = f"/{parts[0]}"
            for param in parts[1::]:
                self.__parameters.append(param)

    @property
    def raw(self):
        return self.__raw

    @property
    def base(self):
        return self.__base

    @base.setter
    def base(self, value):
        self.__base = value

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        self.__parameters = value
