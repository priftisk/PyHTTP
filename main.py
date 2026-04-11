from server.server import Server
from config.config import Config

if __name__ == "__main__":
    config: Config = Config()
    s: Server = Server(config=config)
    s.run()
