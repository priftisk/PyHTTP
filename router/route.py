class Route:
    def __init__(self, route_dict):

        self.__path = route_dict["path"]
        self.__html = route_dict["html"]

    @property
    def path(self):
        return self.__path

    @property
    def html(self):
        return self.__html

    @path.setter
    def path(self, value):
        self.__path = value

    @html.setter
    def html(self, value):
        self.__html = value
