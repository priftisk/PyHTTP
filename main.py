from server.server import Server
from config.config import Config
from handlers import index_handler, posts_handler

if __name__ == "__main__":
    config: Config = Config()
    s: Server = Server(config=config)
    s.router.register_route(["GET", "POST"], "/", index_handler)
    s.router.register_route(["GET"], "/posts", posts_handler)
    s.run()
