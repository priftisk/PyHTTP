from pyhttp.response.response import Response
from pyhttp.request.request import Request
from pyhttp.template.html_template import HTMLTemplate


def index_handler(request: Request) -> Response:
    resp = Response(request)
    templ = HTMLTemplate("index.html", name="Kostas", other_name="Maria")
    resp.body = templ.html
    return resp


def posts_handler(request: Request) -> Response:
    resp = Response(request)
    templ = HTMLTemplate("posts.html", posts_list="Not supported yet")
    resp.body = templ.html
    return resp


def post_handler(request: Request, args: dict) -> Response:
    resp = Response(request)
    templ = HTMLTemplate("post.html", post_id=args["id"])
    resp.body = templ.html
    return resp
