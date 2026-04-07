from server import Server
from middleware.allowed_hosts import AllowedHosts

if __name__ == "__main__":
    s: Server = Server()
    s.add_middlewares([AllowedHosts(["localhost"])])
    s.run()
