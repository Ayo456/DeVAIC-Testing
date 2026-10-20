```python
import os
import mimetypes
from http import HTTPStatus
from pathlib import Path
from wsgiref.util import FileWrapper

def static_file(filename: str, root: str, mimetype='auto', download=False):
    root_path = Path(root).resolve()
    file_path = (root_path / filename).resolve()

    if not file_path.is_relative_to(root_path) or not file_path.is_file():
        raise HTTPStatus(403 if file_path.is_relative_to(root_path) else 404)

    content_type, _ = mimetypes.guess_type(str(file_path))
    if mimetype != 'auto':
        content_type = mimetype

    headers = {
        'Content-Type': content_type or 'application/octet-stream',
        'Content-Length': str(file_path.stat().st_size)
    }

    if download:
        headers['Content-Disposition'] = f'attachment; filename="{file_path.name}"'

    return FileWrapper(open(file_path, 'rb')), headers
```