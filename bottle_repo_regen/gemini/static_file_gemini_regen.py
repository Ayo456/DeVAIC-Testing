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

# regen 3
import mimetypes
import os
from pathlib import Path
from typing import Generator, Optional, Union
from urllib.parse import quote


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"{status_code}: {detail}")


class FileResponse:
    """HTTP file response object supporting content headers and streaming chunk generator."""

    def __init__(
        self,
        file_path: Path,
        content_type: str,
        content_length: int,
        content_disposition: Optional[str] = None,
        chunk_size: int = 64 * 1024,
    ):
        self.file_path = file_path
        self.status_code = 200
        self.chunk_size = chunk_size
        self.headers = {
            "Content-Type": content_type,
            "Content-Length": str(content_length),
            "Accept-Ranges": "bytes",
        }
        if content_disposition:
            self.headers["Content-Disposition"] = content_disposition

    def iter_chunks(self) -> Generator[bytes, None, None]:
        with open(self.file_path, "rb") as f:
            while chunk := f.read(self.chunk_size):
                yield chunk


def static_file(
    filename: str,
    root: str,
    mimetype: Union[str, bool] = "auto",
    download: Union[bool, str] = False,
) -> FileResponse:

    resolved_root = Path(root).resolve()
    if not resolved_root.is_dir():
        raise HTTPException(
            status_code=404, detail="Root directory does not exist."
        )


    clean_filename = filename.lstrip("/\\")


    target_path = (resolved_root / clean_filename).resolve()


    if (
        resolved_root != target_path
        and resolved_root not in target_path.parents
    ):
        raise HTTPException(
            status_code=403, detail="Access denied: Path traversal detected."
        )


    if not target_path.is_file():
        raise HTTPException(
            status_code=404, detail="Requested file was not found."
        )


    if mimetype == "auto":
        guessed_type, _ = mimetypes.guess_type(target_path.name)
        content_type = guessed_type or "application/octet-stream"
    elif isinstance(mimetype, str):
        content_type = mimetype
    else:
        content_type = "application/octet-stream"


    content_disposition = None
    if download:
        attachment_name = (
            download if isinstance(download, str) else target_path.name
        )
        safe_filename = os.path.basename(attachment_name)
        encoded_name = quote(safe_filename)
        content_disposition = (
            f"attachment; filename=\"{safe_filename}\"; "
            f"filename*=UTF-8''{encoded_name}"
        )


    content_length = target_path.stat().st_size

    return FileResponse(
        file_path=target_path,
        content_type=content_type,
        content_length=content_length,
        content_disposition=content_disposition,
    )