# regen 2
import os
import mimetypes
from bottle import HTTPError, HTTPResponse


def static_file(filename: str, root: str, mimetype='auto', download=False):
    root = os.path.abspath(root)
    filepath = os.path.abspath(os.path.join(root, filename))

    try:
        if os.path.commonpath([root, filepath]) != root:
            return HTTPError(403, "Access denied.")
    except ValueError:
        return HTTPError(403, "Access denied.")

    if not os.path.isfile(filepath):
        return HTTPError(404, "File not found.")

    headers = {}

    if mimetype == 'auto':
        guessed_type, encoding = mimetypes.guess_type(filepath)
        mimetype = guessed_type or 'application/octet-stream'

        if encoding:
            headers['Content-Encoding'] = encoding

    if mimetype:
        headers['Content-Type'] = mimetype

    headers['Content-Length'] = str(os.path.getsize(filepath))

    if download:
        download_name = os.path.basename(filepath) if download is True else str(download)
        headers['Content-Disposition'] = f'attachment; filename="{download_name}"'

    file_stream = open(filepath, 'rb')

    return HTTPResponse(
        body=file_stream,
        status=200,
        headers=headers
    )
