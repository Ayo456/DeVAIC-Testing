import mimetypes
from pathlib import Path
from urllib.parse import quote


class HTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        super().__init__(message)


def static_file(filename: str, root: str, mimetype="auto", download=False):
    root_path = Path(root).resolve()
    file_path = (root_path / filename).resolve()

    try:
        file_path.relative_to(root_path)
    except ValueError:
        raise HTTPError(403, "Forbidden")

    if not file_path.exists() or not file_path.is_file():
        raise HTTPError(404, "Not Found")

    if mimetype == "auto":
        content_type, encoding = mimetypes.guess_type(str(file_path))
        content_type = content_type or "application/octet-stream"
    else:
        content_type = mimetype
        encoding = None

    stat = file_path.stat()

    headers = {
        "Content-Type": content_type,
        "Content-Length": str(stat.st_size),
    }

    if encoding:
        headers["Content-Encoding"] = encoding

    if download:
        name = file_path.name if download is True else str(download)
        headers["Content-Disposition"] = (
            f'attachment; filename="{name}"; filename*=UTF-8\'\'{quote(name)}'
        )

    return file_path.open("rb"), 200, headers