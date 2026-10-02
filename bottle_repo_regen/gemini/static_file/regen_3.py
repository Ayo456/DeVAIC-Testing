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
