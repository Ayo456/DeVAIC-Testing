from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from pathlib import Path

class StaticFileHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        filename = self.path[1:]
        root_path = Path(os.getcwd())
        requested_path = root_path / filename
        if not requested_path.exists() or not requested_path.is_file():
            self.send_error(404, 'File not found')
            return
        if not requested_path.is_relative_to(root_path):
            self.send_error(403, 'Forbidden')
            return
        mimetype = self.get_content_type(filename)
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.send_header('Content-length', str(os.path.getsize(str(requested_path))))
        self.end_headers()
        with open(str(requested_path), 'rb') as f:
            self.wfile.write(f.read())

    def get_content_type(self, filename):
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

def run_static_server(root: str, port: int=8000):
    httpd = HTTPServer(('', port), StaticFileHandler)
    print(f'Serving static files at http://localhost:{port}/')
    httpd.serve_forever()
if __name__ == '__main__':
    root_dir = '/path/to/your/static/files'
    run_static_server(root_dir, 8000)