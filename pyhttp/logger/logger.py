from datetime import datetime


class Logger:

    def writer(func: function):
        def wrapper(*args, **kwargs):
            f_name = func.__name__
            log_msg = [arg for arg in args if isinstance(arg, str)]
            if len(log_msg) != 1:
                raise Exception("Must be provided with exactly one message.")

            match f_name:
                case "info":
                    level_symbol = "*"
                case "error":
                    level_symbol = "!"
                case _:
                    level_symbol = "*"
            print(
                f"[{level_symbol}] [{datetime.today().strftime("%d/%m/%Y %H:%M:%S")}] {log_msg[0]}"
            )

        return wrapper

    def __init__(self):
        pass

    @writer
    def error(self, msg: str):
        pass

    @writer
    def info(self, msg: str):
        pass
