# regen 1
from pathlib import Path
import mimetypes
from flask import abort, send_file


def static_file(filename: str, root: str, mimetype='auto', download=False):
    root_path = Path(root).resolve()
    file_path = (root_path / filename).resolve()

    try:
        file_path.relative_to(root_path)
    except ValueError:
        abort(403)

    if not file_path.exists() or not file_path.is_file():
        abort(404)

    if mimetype == 'auto':
        detected_type, _ = mimetypes.guess_type(str(file_path))
        mimetype = detected_type or 'application/octet-stream'

    return send_file(
        file_path,
        mimetype=mimetype,
        as_attachment=bool(download),
        download_name=file_path.name if download else None
    )

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

# regen 3
from pathlib import Path
from starlette.responses import FileResponse
from starlette.exceptions import HTTPException


def static_file(filename: str, root: str, mimetype="auto", download=False):
    root_path = Path(root).resolve()

    try:
        file_path = (root_path / filename).resolve()
        file_path.relative_to(root_path)
    except (ValueError, OSError):
        raise HTTPException(status_code=403, detail="Forbidden")

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        stat_result = file_path.stat()
    except OSError:
        raise HTTPException(status_code=404, detail="File not found")

    media_type = None if mimetype == "auto" else mimetype

    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        filename=file_path.name if download else None,
        stat_result=stat_result
    )