from .route import Route
from request.request import Request
from request.request_methods import RequestMethod
from response.response import Response


class Router:
    def __init__(self):
        self.__routes: list[Route] = []

    @property
    def routes(self):
        return self.__routes

    @routes.setter
    def routes(self, value):
        self.__routes = value

    def register_route(
        self, methods: list[RequestMethod], path: str, handler: function
    ):
        self.__routes.append(Route(methods=methods, path=path, handler=handler))

    def request_method_allowed(
        self, request: Request, allowed_methods: list[RequestMethod]
    ):
        return request.method in allowed_methods

    def invoke_handler(self, request: Request):
        for route in self.routes:
            if route.path == request.path:
                if not route.method_allowed(request.method):
                    return Response(request, 405)  # Method not allowed
                return route.handler(request)  # Succesful match
        return Response(request, 404)  # Route does not exist

    def show_routes(self):
        print("-----------ROUTES-----------")
        for route in self.routes:
            print(f"{route.path} -> {route.html}")

    def route_exists(self, route) -> bool:
        for r in self.routes:
            if r.path == route:
                return True
        return False
