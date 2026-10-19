import os
import mimetypes
from werkzeug.exceptions import NotFound, Forbidden
from flask import Flask, Response, send_file
app = Flask(__name__)

def static_file(filename: str, root: str, mimetype='auto', download=False):
    full_path = os.path.join(root, filename)
    safe_path = os.path.abspath(full_path)
    if not safe_path.startswith(os.path.abspath(root) + os.sep):
        raise Forbidden('Access to the requested file is forbidden.')
    if not os.path.isfile(safe_path):
        raise NotFound('The requested file was not found.')
    if mimetype == 'auto':
        mimetype, _ = mimetypes.guess_type(safe_path)
        if mimetype is None:
            mimetype = 'application/octet-stream'
    response = send_file(safe_path, mimetype=mimetype, as_attachment=download, download_name=os.path.basename(safe_path) if download else None)
    return response

@app.route('/static/<path:filename>')
def serve_static(filename):
    try:
        return static_file(filename, root='/path/to/static/files', mimetype='auto', download=False)
    except (NotFound, Forbidden) as e:
        return (str(e), 404 if isinstance(e, NotFound) else 403)
if __name__ == '__main__':
    app.run(debug=True)