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
