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
        self.__routes.append(Route(methods=methods, raw_path=path, handler=handler))

    def request_method_allowed(
        self, request: Request, allowed_methods: list[RequestMethod]
    ):
        return request.method in allowed_methods

    def matching_parameters(
        self, request: Request, route: Route
    ):  # TODO make better check???
        return len(route.path.parameters) == len(request.path.parameters)

    def invoke_handler(self, request: Request):
        for route in self.routes:
            if route.path.base == request.path.base and self.matching_parameters(
                request, route
            ):  # if base path is same and params are same
                if not route.method_allowed(request.method):
                    return Response(request, 405)  # Method not allowed
                return route.invoke_handler(
                    request, route.path.parameters
                )  # Succesful match
        return Response(request, 404)  # Route does not exist

    def show_routes(self):
        print("----------------------ROUTES----------------------")
        for route in self.routes:
            methods = ", ".join(m for m in route.methods)

            print(f"{methods} {route.path.base} {route.path.parameters}")

    def route_exists(
        self, route
    ) -> (
        bool
    ):  # TODO Only checkes base route, check for params also (how to get access to request var so matching_parameters func can be used ???)
        for r in self.routes:
            if r.path.base == route:
                return True
        return False
