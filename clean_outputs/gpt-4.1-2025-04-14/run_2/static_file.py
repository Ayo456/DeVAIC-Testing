import os
import mimetypes
import email.utils
import time
import re

def static_file(filename, root, mimetype='auto', download=False, charset='UTF-8'):
    try:
        fname = filename.strip('/\\')
        root = os.path.abspath(root)
        abspath = os.path.abspath(os.path.join(root, fname))
        if not abspath.startswith(root + os.sep) and abspath != root:
            return HTTPError(403, 'Forbidden')
        if not os.path.exists(abspath) or not os.path.isfile(abspath):
            return HTTPError(404, 'File not found')
        if not os.access(abspath, os.R_OK):
            return HTTPError(403, 'Forbidden')
        stat = os.stat(abspath)
        file_size = stat.st_size
        mtime = stat.st_mtime
        last_modified = email.utils.formatdate(mtime, usegmt=True)
        headers = {}
        guessed_type, guessed_encoding = (None, None)
        if mimetype == 'auto':
            guessed_type, guessed_encoding = mimetypes.guess_type(abspath)
            ctype = guessed_type or 'application/octet-stream'
            if guessed_encoding:
                headers['Content-Encoding'] = guessed_encoding
        else:
            ctype = mimetype
        if ctype.startswith('text/') and 'charset=' not in ctype and charset:
            ctype += f'; charset={charset}'
        headers['Content-Type'] = ctype
        if download:
            if isinstance(download, str):
                dispname = os.path.basename(download)
            else:
                dispname = os.path.basename(abspath)
            headers['Content-Disposition'] = f'attachment; filename="{dispname}"'
        headers['Content-Length'] = str(file_size)
        headers['Last-Modified'] = last_modified
        headers['Accept-Ranges'] = 'bytes'
        ims = request.environ.get('HTTP_IF_MODIFIED_SINCE')
        if ims:
            try:
                ims_time = email.utils.parsedate_to_datetime(ims)
                if ims_time.tzinfo is None:
                    ims_time = ims_time.replace(tzinfo=time.timezone)
                file_time = email.utils.parsedate_to_datetime(last_modified)
                if file_time <= ims_time:
                    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
                    return HTTPResponse('', 304, **headers)
            except Exception:
                pass
        range_header = request.environ.get('HTTP_RANGE')
        if range_header:
            m = re.match('bytes=(\\d*)-(\\d*)', range_header)
            if m:
                start_str, end_str = m.groups()
                if start_str == '' and end_str == '':
                    return HTTPError(416, 'Range Not Satisfiable')
                if start_str == '':
                    length = int(end_str)
                    if length == 0:
                        return HTTPError(416, 'Range Not Satisfiable')
                    start = file_size - length
                    end = file_size - 1
                else:
                    start = int(start_str)
                    if end_str == '':
                        end = file_size - 1
                    else:
                        end = int(end_str)
                if start > end or start < 0 or end >= file_size:
                    return HTTPError(416, 'Range Not Satisfiable')
                length = end - start + 1
                headers['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                headers['Content-Length'] = str(length)
                status = 206
                if request.method == 'HEAD':
                    body = ''
                else:
                    f = open(abspath, 'rb')
                    f.seek(start)
                    body = f.read(length)
                    f.close()
                return HTTPResponse(body, status, **headers)
            else:
                return HTTPError(416, 'Range Not Satisfiable')
        if request.method == 'HEAD':
            body = ''
        else:
            body = open(abspath, 'rb')
        return HTTPResponse(body, 200, **headers)
    except Exception:
        return HTTPError(500, 'Internal Server Error')