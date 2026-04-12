SERVER_HOST = "0.0.0.0"
SERVER_PORT = 9999
ALLOWED_HOSTS = ["localhot"]

MIDDLEWARE = ["middleware.allowed_hosts.AllowedHosts"]

ROUTES = [{"path": "/", "html": "index.html"}, {"path": "/posts", "html": "posts.html"}]
