from server import Server
from middleware.allowed_hosts import AllowedHosts
from config.config import Config

if __name__ == "__main__":
    config: Config = Config()
    config.parse()
    s: Server = Server(config=config)
    # s.add_middlewares([AllowedHosts(["localhost"])])
    s.run()
