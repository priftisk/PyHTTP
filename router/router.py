from helper.filereader import Filereader
from .route import Route


class Router:
    def __init__(self):
        try:
            from settings import ROUTES

            self.__routes: list[Route] = []
            for route in ROUTES:
                self.__routes.append(Route(route))
        except ImportError as e:
            raise Exception(e.msg)
        finally:
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
        for route in self.routes:
            print(f"{route.path} -> {route.html}")

    def route_exists(self, route):
        for r in self.routes:
            if r.path == route:
                return True
        return False

    def get_html_from_path(self, route):
        for r in self.routes:
            if r.path == route:
                return r.html
        return None

    def route_to_html(self, route):
        html_file = self.get_html_from_path(route)
        if not html_file:
            raise Exception(
                f"No matching html file for route: {route}",
            )
        html = self.filereader.read(filepath=html_file).encode()
        return html
