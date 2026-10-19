from flask import Flask, send_from_directory, abort
import os
import mimetypes
app = Flask(__name__)

def static_file(filename: str, root: str, mimetype='auto', download=False):
    full_path = os.path.join(root, filename)
    if not os.path.commonpath([os.path.abspath(root), os.path.abspath(full_path)]) == os.path.abspath(root):
        abort(403)
    if not os.path.isfile(full_path):
        abort(404)
    if mimetype == 'auto':
        mimetype, _ = mimetypes.guess_type(filename)
    as_attachment = download
    return send_from_directory(root, filename, mimetype=mimetype, as_attachment=as_attachment, download_name=filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    root = '/path/to/your/static/files'
    return static_file(filename, root)
if __name__ == '__main__':
    app.run(debug=True)