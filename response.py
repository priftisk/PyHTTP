class Response:
    def __init__(self, request):
        self.__request= request
    
    def encode(self):
        return """
HTTP/1.1 201 Created
Content-Type: application/html

<html><body>Hello World</body></html>

""".encode()
