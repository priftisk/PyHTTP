from helper.filereader import Filereader
from .route import Route
from request.request import Request


class Router:
    def __init__(self):
        try:
            self.__routes: list[Route] = []
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

    def register_route(self, path: str, handler: function):
        self.__routes.append(Route(path=path, handler=handler))

    def invoke_handler(self, request: Request):
        for r in self.routes:
            if r.path == request.path:
                return r.handler(request)

    def show_routes(self):
        print("-----------ROUTES-----------")
        for route in self.routes:
            print(f"{route.path} -> {route.html}")

    def route_exists(self, route) -> bool:
        for r in self.routes:
            if r.path == route:
                return True
        return False

    def get_html_from_path(self, route) -> str | None:
        for r in self.routes:
            if r.path == route:
                return r.html
        return None

    def path_to_html(self, path) -> str:
        html_file = self.get_html_from_path(path)
        if not html_file:
            raise Exception(
                f"No matching html file for route: {path}",
            )
        html = self.filereader.read(filepath=html_file).encode()
        return html
