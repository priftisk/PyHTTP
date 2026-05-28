# PyHTTP

A lightweight HTTP server framework written in Python — **no third-party dependencies**. PyHTTP is built entirely on Python's standard library, making it easy to understand, extend, and deploy without a single `pip install`.

## Features

- **Routing** — Register URL routes and map them to handler functions
- **Request parsing** — Structured access to incoming HTTP request data
- **Response building** — Helpers for constructing and sending HTTP responses
- **Middleware** — Chain middleware functions to process requests and responses
- **Template rendering** — Serve dynamic HTML views from the `views/` directory
- **Logging** — Built-in request logging with no external logging libraries
- **Configuration** — Centralised server config via `settings.py` and the `Config` class

## Getting Started

```bash
git clone https://github.com/priftisk/PyHTTP.git
cd PyHTTP
make run
```

No virtual environment or package installation required.

## Usage

Register routes and start the server in `main.py`:

```python
from server.server import Server
from config.config import Config
from handlers import index_handler, posts_handler, post_handler

if __name__ == "__main__":
    config: Config = Config()
    s: Server = Server(config=config)
    s.router.register_route(["GET", "POST"], "/", index_handler)
    s.router.register_route(["GET"], "/posts", posts_handler)
    s.router.register_route(["GET"], "/posts/:id", post_handler)
    s.run()
```

## Project Structure

```
PyHTTP/
├── server/       # Core HTTP server
├── router/       # URL routing
├── request/      # Request parsing
├── response/     # Response construction
├── middleware/   # Middleware pipeline
├── template/     # Template engine
├── logger/       # Request logging
├── config/       # Server configuration
├── helper/       # Utility functions
├── views/        # HTML templates
└── main.py       # Entry point
```

## Requirements

Python 3.x — standard library only.
