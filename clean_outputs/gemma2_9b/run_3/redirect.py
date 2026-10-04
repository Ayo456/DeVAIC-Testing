from http.server import HTTPServer, BaseHTTPRequestHandler

class RedirectHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(code or 303)
        self.send_header('Location', self.path)
        self.end_headers()

def redirect(url: str, code: int=None) -> None:
    server = HTTPServer(('', 8000), RedirectHandler)
    server.serve_forever()