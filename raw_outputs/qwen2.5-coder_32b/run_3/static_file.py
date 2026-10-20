```python
import os
import mimetypes
from http import HTTPStatus
from wsgiref.util import FileWrapper
from werkzeug.exceptions import NotFound, Forbidden
from werkzeug.wrappers import Response

def static_file(filename: str, root: str, mimetype='auto', download=False):
    safe_path = os.path.abspath(os.path.join(root, filename))
    if not safe_path.startswith(os.path.abspath(root) + os.sep):
        raise Forbidden(description="Access to the requested resource is forbidden.")
    if not os.path.exists(safe_path) or not os.path.isfile(safe_path):
        raise NotFound(description="The requested file was not found.")
    guessed_type, _ = mimetypes.guess_type(safe_path)
    content_type = guessed_type if mimetype == 'auto' else mimetype
    headers = {'Content-Type': content_type}
    if download:
        headers['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
    return Response(FileWrapper(open(safe_path, 'rb')), headers=headers, status=HTTPStatus.OK)
```