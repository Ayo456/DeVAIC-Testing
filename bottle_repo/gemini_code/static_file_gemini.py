import mimetypes
import os
from typing import Generator, Union


class HTTPError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


class StaticResponse:
    def __init__(
        self,
        filepath: str,
        content_type: str,
        content_length: int,
        download_name: Union[str, None] = None,
    ):
        self.filepath = filepath
        self.status = 200
        self.headers = {
            "Content-Type": content_type,
            "Content-Length": str(content_length),
        }
        if download_name:
            self.headers["Content-Disposition"] = (
                f'attachment; filename="{download_name}"'
            )

    def iter_body(self, chunk_size: int = 65536) -> Generator[bytes, None, None]:
        with open(self.filepath, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk


def static_file(
    filename: str, root: str, mimetype: str = "auto", download: Union[bool, str] = False
) -> StaticResponse:
    root_path = os.path.abspath(root)

    safe_filename = filename.lstrip(r"\/")
    target_path = os.path.abspath(os.path.join(root_path, safe_filename))

    try:
        common = os.path.commonpath([root_path, target_path])
    except ValueError:
        raise HTTPError(403, "Access denied")

    if common != root_path:
        raise HTTPError(403, "Access denied")

    if not os.path.isfile(target_path):
        raise HTTPError(404, "File not found")

    if mimetype == "auto":
        guessed_type, _ = mimetypes.guess_type(target_path)
        content_type = guessed_type or "application/octet-stream"
    else:
        content_type = mimetype

    content_length = os.path.getsize(target_path)

    download_name = None
    if download is True:
        download_name = os.path.basename(target_path)
    elif isinstance(download, str):
        download_name = download

    return StaticResponse(
        filepath=target_path,
        content_type=content_type,
        content_length=content_length,
        download_name=download_name,
    )