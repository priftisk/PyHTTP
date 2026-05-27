from server.server import Server
from config.config import Config
from handlers import index_handler

if __name__ == "__main__":
    config: Config = Config()
    s: Server = Server(config=config)
    s.router.register_route("/", index_handler)
    s.run()
