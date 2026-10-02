# regen 1
import mimetypes
import os
from pathlib import Path
from typing import BinaryIO, Dict, Union


class HTTPError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


class FileResponse:
    def __init__(self, file_path: Path, headers: Dict[str, str], status_code: int = 200):
        self.file_path = file_path
        self.headers = headers
        self.status_code = status_code

    def open(self) -> BinaryIO:
        """Returns a binary stream of the file content."""
        return open(self.file_path, "rb")


def static_file(
    filename: str,
    root: str,
    mimetype: str = "auto",
    download: Union[bool, str] = False,
) -> FileResponse:
    """
    Validates and serves a static file from a root directory.

    Guards against path traversal attacks by resolving symlinks and verifying
    that the target path remains inside root. Configures standard HTTP headers
    and returns a FileResponse stream wrapper. Raises HTTPError (403/404) on failure.
    """
    try:
        resolved_root = Path(root).resolve(strict=True)
    except (FileNotFoundError, NotADirectoryError):
        raise HTTPError(404, "Root directory not found")

    if not resolved_root.is_dir():
        raise HTTPError(404, "Root path is not a directory")


    clean_filename = filename.lstrip("/\\")
    target_path = resolved_root.joinpath(clean_filename)

    try:
        resolved_file = target_path.resolve(strict=True)
    except FileNotFoundError:
        raise HTTPError(404, "File not found")
    except (PermissionError, RuntimeError):
        raise HTTPError(403, "Access denied")


    try:
        resolved_file.relative_to(resolved_root)
    except ValueError:
        raise HTTPError(403, "Directory traversal detected")

    if not resolved_file.is_file():
        raise HTTPError(404, "Target path is not a regular file")


    if mimetype == "auto":
        guessed_type, encoding = mimetypes.guess_type(resolved_file)
        content_type = guessed_type or "application/octet-stream"
    else:
        content_type = mimetype

    file_size = resolved_file.stat().st_size

    headers = {
        "Content-Type": content_type,
        "Content-Length": str(file_size),
    }


    if download:
        attachment_name = download if isinstance(download, str) else resolved_file.name
        headers["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment_name)}"'

    return FileResponse(file_path=resolved_file, headers=headers, status_code=200)
