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
