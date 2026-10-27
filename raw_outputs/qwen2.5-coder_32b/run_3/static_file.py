```python
import os
import mimetypes
from datetime import datetime
from email.utils import formatdate
from urllib.parse import unquote

def static_file(filename, root, mimetype='auto', download=False, charset='UTF-8'):
    filename = unquote(filename.strip('/\\'))
    filepath = os.path.join(root, filename)
    if not os.path.commonpath([os.path.abspath(filepath), os.path.abspath(root)]) == os.path.abspath(root):
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
    headers['Content-Type'] = mimetype or 'application/octet-stream'
    
    if download:
        if isinstance(download, str):
            download = os.path.basename(download)
        else:
            download = os.path.basename(filepath)
        headers['Content-Disposition'] = f'attachment; filename="{download}"'
    
    file_stat = os.stat(filepath)
    headers['Content-Length'] = str(file_stat.st_size)
    headers['Last-Modified'] = formatdate(file_stat.st_mtime, usegmt=True)
    headers['Accept-Ranges'] = 'bytes'
    
    if 'If-Modified-Since' in request.environ:
        if_modified_since = request.environ['If-Modified-Since']
        if datetime.strptime(if_modified_since, '%a, %d %b %Y %H:%M:%S %Z') >= datetime.utcfromtimestamp(file_stat.st_mtime):
            headers['Date'] = formatdate(usegmt=True)
            return HTTPResponse(status=304, **headers)
    
    if request.method == 'HEAD':
        return HTTPResponse(status=200, **headers)
    
    if 'Range' in request.environ:
        range_header = request.environ['Range']
        if range_header.startswith('bytes='):
            range_header = range_header[6:]
            ranges = range_header.split(',')
            for range_spec in ranges:
                range_spec = range_spec.strip()
                if '-' in range_spec:
                    start, end = range_spec.split('-', 1)
                    start = int(start) if start else 0
                    end = int(end) if end else file_stat.st_size - 1
                    if 0 <= start < file_stat.st_size and 0 <= end < file_stat.st_size and start <= end:
                        with open(filepath, 'rb') as f:
                            f.seek(start)
                            body = f.read(end - start + 1)
                        headers['Content-Range'] = f'bytes {start}-{end}/{file_stat.st_size}'
                        headers['Content-Length'] = str(end - start + 1)
                        return HTTPResponse(body=body, status=206, **headers)
        return HTTPError(416, 'Requested Range Not Satisfiable')
    
    with open(filepath, 'rb') as f:
        body = f.read()
    return HTTPResponse(body=body, status=200, **headers)
```