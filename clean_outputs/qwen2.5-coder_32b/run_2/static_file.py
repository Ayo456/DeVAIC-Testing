import os
import mimetypes
from datetime import datetime, timezone
from email.utils import format_datetime

def static_file(filename, root, mimetype='auto', download=False, charset='UTF-8'):
    filename = filename.strip('/\\')
    filepath = os.path.join(root, filename)
    abs_filepath = os.path.abspath(filepath)
    abs_root = os.path.abspath(root)
    if not abs_filepath.startswith(abs_root + os.sep):
        return HTTPError(403, 'Forbidden')
    if not os.path.isfile(abs_filepath):
        return HTTPError(404, 'Not Found')
    if not os.access(abs_filepath, os.R_OK):
        return HTTPError(403, 'Forbidden')
    file_stat = os.stat(abs_filepath)
    last_modified = format_datetime(datetime.fromtimestamp(file_stat.st_mtime, timezone.utc))
    if mimetype == 'auto':
        mimetype, encoding = mimetypes.guess_type(abs_filepath)
        if encoding:
            headers = {'Content-Encoding': encoding}
        else:
            headers = {}
    else:
        headers = {}
    if mimetype and mimetype.startswith('text/') and charset:
        mimetype += f'; charset={charset}'
    headers['Content-Type'] = mimetype if mimetype else 'application/octet-stream'
    headers['Content-Length'] = str(file_stat.st_size)
    headers['Last-Modified'] = last_modified
    headers['Accept-Ranges'] = 'bytes'
    if_modified_since = request.environ.get('HTTP_IF_MODIFIED_SINCE')
    if if_modified_since and last_modified <= if_modified_since:
        headers['Date'] = format_datetime(datetime.now(timezone.utc))
        return HTTPResponse(status=304, **headers)
    if request.method == 'HEAD':
        return HTTPResponse(status=200, **headers)
    try:
        file_range = request.environ.get('HTTP_RANGE')
        if file_range:
            start, end = (0, file_stat.st_size - 1)
            if file_range.startswith('bytes='):
                range_spec = file_range[len('bytes='):].split('-', 1)
                if range_spec[0]:
                    start = int(range_spec[0])
                if range_spec[1]:
                    end = int(range_spec[1])
                if start < 0 or end >= file_stat.st_size or start > end:
                    headers['Content-Range'] = f'bytes */{file_stat.st_size}'
                    return HTTPError(416, 'Requested Range Not Satisfiable', **headers)
                headers['Content-Range'] = f'bytes {start}-{end}/{file_stat.st_size}'
                headers['Content-Length'] = str(end - start + 1)
                return HTTPResponse(status=206, **headers, body=open(abs_filepath, 'rb').read(start, end - start + 1))
    except ValueError:
        pass
    if download:
        if isinstance(download, str):
            filename = os.path.basename(download)
        else:
            filename = os.path.basename(filepath)
        headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return HTTPResponse(status=200, **headers, body=open(abs_filepath, 'rb'))