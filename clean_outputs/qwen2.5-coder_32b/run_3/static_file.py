import os
import mimetypes
from flask import Flask, send_file, abort
app = Flask(__name__)

def static_file(filename: str, root: str, mimetype='auto', download=False):
    root = os.path.abspath(root)
    full_path = os.path.join(root, filename)
    normalized_path = os.path.normpath(full_path)
    if not normalized_path.startswith(root):
        abort(403)
    if not os.path.isfile(normalized_path):
        abort(404)
    if mimetype == 'auto':
        mimetype, _ = mimetypes.guess_type(normalized_path)
        if mimetype is None:
            mimetype = 'application/octet-stream'
    as_attachment = filename if download else False
    return send_file(normalized_path, mimetype=mimetype, as_attachment=as_attachment)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return static_file(filename, '/path/to/static/files')
if __name__ == '__main__':
    app.run(debug=True)