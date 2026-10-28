import os
import mimetypes
from email.utils import formatdate
from urllib.parse import unquote

def static_file(filename, root, mimetype='auto', download=False, charset='UTF-8'):
    filename = unquote(filename.strip('/\\'))
    filepath = os.path.join(root, filename)
    if not os.path.commonpath([os.path.abspath(root), os.path.abspath(filepath)]) == os.path.abspath(root):
        return HTTPError(403, 'Forbidden')
    if not os.path.isfile(filepath):
        return HTTPError(404, 'Not Found')
    if not os.access(filepath, os.R_OK):
        return HTTPError(403, 'Forbidden')
    if mimetype == 'auto':
        mimetype, encoding = mimetypes.guess_type(filepath)
        if encoding:
            headers = {'Content-Encoding': encoding}
        else:
            headers = {}
    else:
        headers = {}
    if mimetype and mimetype.startswith('text/') and charset:
        mimetype += f'; charset={charset}'
    headers['Content-Length'] = str(os.path.getsize(filepath))
    headers['Last-Modified'] = formatdate(os.path.getmtime(filepath), usegmt=True)
    headers['Accept-Ranges'] = 'bytes'
    if 'If-Modified-Since' in request.environ:
        if_modified_since = request.environ['If-Modified-Since']
        if formatdate(os.path.getmtime(filepath), usegmt=True) <= if_modified_since:
            headers['Date'] = formatdate(usegmt=True)
            return HTTPResponse(status=304, **headers)
    if request.method == 'HEAD':
        return HTTPResponse(status=200, **headers)
    if 'Range' in request.environ:
        try:
            range_header = request.environ['Range']
            start, end = range_header.strip().split('=')[1].split('-')
            start = int(start) if start else 0
            end = int(end) if end else None
        except ValueError:
            return HTTPError(416, 'Range Not Satisfiable')
        file_size = os.path.getsize(filepath)
        if end is None:
            end = file_size - 1
        if start < 0 or end >= file_size or start > end:
            return HTTPError(416, 'Range Not Satisfiable')
        headers['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        headers['Content-Length'] = str(end - start + 1)
        with open(filepath, 'rb') as f:
            f.seek(start)
            body = f.read(end - start + 1)
        return HTTPResponse(body=body, status=206, **headers)
    if download:
        if isinstance(download, str):
            filename = os.path.basename(download)
        else:
            filename = os.path.basename(filepath)
        headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    with open(filepath, 'rb') as f:
        body = f.read()
    return HTTPResponse(body=body, status=200, **headers)