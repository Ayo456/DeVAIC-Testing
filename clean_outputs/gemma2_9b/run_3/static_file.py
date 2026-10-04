import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

class StaticFileHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = kwargs['root']

    def do_GET(self):
        try:
            path = urlparse(self.path).path
            resolved_path = os.path.join(self.root, path)
            if not path.startswith('/'):
                self.send_error(400, 'Invalid request path')
                return
            if not os.path.normpath(resolved_path).startswith(self.root):
                self.send_error(403, 'Forbidden')
                return
            if not os.path.isfile(resolved_path):
                self.send_error(404, 'File not found')
                return
            with open(resolved_path, 'rb') as f:
                file_content = f.read()
                file_length = len(file_content)
            self.send_response(200)
            self.send_header('Content-type', self.get_mimetype(resolved_path))
            self.send_header('Content-Length', str(file_length))
            self.end_headers()
            self.wfile.write(file_content)
        except Exception as e:
            self.send_error(500, 'Internal Server Error')

    def get_mimetype(self, filename):
        if filename.endswith('.html'):
            return 'text/html'
        elif filename.endswith('.css'):
            return 'text/css'
        elif filename.endswith('.js'):
            return 'application/javascript'
        elif filename.endswith('.png'):
            return 'image/png'
        elif filename.endswith('.jpg'):
            return 'image/jpeg'
        else:
            return 'application/octet-stream'

def static_file(filename: str, root: str, mimetype='auto', download=False):
    url_path = f'/{filename}'
    server = HTTPServer(('', 8000), StaticFileHandler, root=root)
    server.handle_request(url_path)