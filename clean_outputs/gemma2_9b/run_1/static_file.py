import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

def static_file(filename: str, root: str, mimetype='auto', download=False):
    try:
        filepath = Path(root, filename)
        if not filepath.is_relative_to(Path(root)):
            raise HTTPError(403, 'Forbidden: File outside root directory')
        with open(filepath, 'rb') as f:
            content = f.read()
        if mimetype == 'auto':
            mimetype = mimetypes.guess_type(filepath)[0]
        headers = {'Content-Type': mimetype, 'Content-Length': len(content)}
        if download:
            headers['Content-Disposition'] = 'attachment; filename=' + filename
        return HTTPResponse(content, headers)
    except FileNotFoundError:
        raise HTTPError(404, 'Not Found: File not found')