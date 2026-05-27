from response.response import Response
from request.request import Request
from template.html_template import HTMLTemplate


def index_handler(request: Request):
    resp = Response(request)
    templ = HTMLTemplate("index.html", name="Kostas", other_name="Maria")
    resp.body = templ.html
    return resp


def posts_handler(request: Request):
    resp = Response(request)
    templ = HTMLTemplate("posts.html", posts_list="Not supported yet")
    resp.body = templ.html
    return resp
