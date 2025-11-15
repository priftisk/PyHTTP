from helper.filereader import Filereader


class Router:
    def __init__(self, routes={}):
        self.__routes: dict = routes
        self.__filereader = Filereader()

    @property
    def filereader(self):
        return self.__filereader

    @property
    def routes(self):
        return self.__routes

    @routes.setter
    def routes(self, value):
        self.__routes = value

    def show_routes(self):
        print("-----------ROUTES-----------")
        for path, html in self.routes.items():
            print(f"{path} -> {html}")

    def route_exists(self, route):
        return self.routes.get(route) is not None

    def route_to_html(self, route):
        html_file = self.routes.get(route)
        if not html_file:
            raise Exception(
                f"No matching html file for route: {route}",
            )
        html = self.filereader.read(filepath=html_file).encode()
        return html
