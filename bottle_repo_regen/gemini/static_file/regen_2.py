# regen 2
from email.utils import formatdate
import mimetypes
from pathlib import Path
from typing import BinaryIO, Generator, Optional, Union
from urllib.parse import quote


class HTTPError(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(f"HTTP {status_code}: {detail}")
        self.status_code = status_code
        self.detail = detail


class FileResponse:
    """Represents a standard HTTP response serving static file content."""

    def __init__(
        self,
        file_path: Path,
        headers: dict[str, str],
        status_code: int = 200,
        chunk_size: int = 64 * 1024,
    ):
        self.file_path = file_path
        self.headers = headers
        self.status_code = status_code
        self.chunk_size = chunk_size

    def iter_content(self) -> Generator[bytes, None, None]:
        """Streams the file in chunks to prevent high memory usage."""
        with open(self.file_path, "rb") as f:
            while chunk := f.read(self.chunk_size):
                yield chunk

    def read(self) -> bytes:
        """Reads and returns the complete binary payload."""
        return self.file_path.read_bytes()


def static_file(
    filename: str,
    root: str,
    mimetype: str = "auto",
    download: Union[bool, str] = False,
) -> FileResponse:
    """Validates and serves a static file from a root directory.

    Ensures the path does not traverse outside the root directory, computes
    standard HTTP headers, and returns a FileResponse stream.

    Raises:
        HTTPError: 403 if the path resolves outside root, is not a regular file,
                   or is inaccessible.
        HTTPError: 404 if the requested file does not exist.
    """
    try:
        base_dir = Path(root).resolve(strict=True)
    except (FileNotFoundError, NotADirectoryError):
        raise HTTPError(404, "Root directory not found")


    clean_filename = filename.lstrip("/\\")
    target_path = (base_dir / clean_filename).resolve()


    try:
        target_path.relative_to(base_dir)
    except ValueError:
        raise HTTPError(403, "Access denied: Directory traversal detected")

    if not target_path.exists():
        raise HTTPError(404, "File not found")

    if not target_path.is_file():
        raise HTTPError(403, "Access denied: Target is not a regular file")

    try:
        stat_result = target_path.stat()
    except PermissionError:
        raise HTTPError(403, "Access denied: Insufficient read permissions")


    if mimetype == "auto":
        guessed_type, _ = mimetypes.guess_type(target_path.name)
        content_type = guessed_type or "application/octet-stream"
    else:
        content_type = mimetype

    headers: dict[str, str] = {
        "Content-Type": content_type,
        "Content-Length": str(stat_result.st_size),
        "Last-Modified": formatdate(stat_result.st_mtime, usegmt=True),
    }


    if download:
        attachment_name = (
            download if isinstance(download, str) else target_path.name
        )
        encoded_name = quote(attachment_name)
        headers["Content-Disposition"] = (
            f'attachment; filename="{attachment_name}"; filename*=UTF-8\'\'{encoded_name}'
        )

    return FileResponse(file_path=target_path, headers=headers)
