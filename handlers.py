from response.response import Response, Request


def index_handler(request: Request):
    print(request.path, "   DIOasgdosa")
    print("INDEX HADNLER")
    return Response(request)
