from pyhttp.server.server import Server
from pyhttp.config.config import Config
from handlers import index_handler, posts_handler, post_handler

if __name__ == "__main__":
    config: Config = Config()
    s: Server = Server(config=config)
    s.router.register_route(["GET", "POST"], "/", index_handler)
    s.router.register_route(["GET"], "/posts", posts_handler)
    s.router.register_route(["GET"], "/posts/:id", post_handler)
    s.run()
