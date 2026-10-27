import os
import mimetypes
import email.utils
import time

def static_file(filename, root, mimetype='auto', download=False, charset='UTF-8'):
    try:
        fname = filename.strip('/\\')
        abspath = os.path.abspath(os.path.join(root, fname))
        root_abs = os.path.abspath(root)
        if not abspath.startswith(root_abs + os.sep) and abspath != root_abs:
            return HTTPError(403, 'Forbidden')
        if not os.path.isfile(abspath):
            return HTTPError(404, 'File not found')
        if not os.access(abspath, os.R_OK):
            return HTTPError(403, 'Forbidden')
        stat = os.stat(abspath)
        file_size = stat.st_size
        mtime = stat.st_mtime
        last_modified = email.utils.formatdate(mtime, usegmt=True)
        headers = {'Last-Modified': last_modified, 'Accept-Ranges': 'bytes'}
        guessed_type, guessed_encoding = (None, None)
        if mimetype == 'auto':
            guessed_type, guessed_encoding = mimetypes.guess_type(abspath)
            content_type = guessed_type or 'application/octet-stream'
            if guessed_encoding:
                headers['Content-Encoding'] = guessed_encoding
        else:
            content_type = mimetype
        if content_type.startswith('text/') and 'charset=' not in content_type and charset:
            content_type += f'; charset={charset}'
        headers['Content-Type'] = content_type
        if download:
            if isinstance(download, str):
                disp_name = os.path.basename(download)
            else:
                disp_name = os.path.basename(abspath)
            headers['Content-Disposition'] = f'attachment; filename="{disp_name}"'
        headers['Content-Length'] = str(file_size)
        ims = request.environ.get('HTTP_IF_MODIFIED_SINCE')
        if ims:
            try:
                ims_time = email.utils.parsedate_to_datetime(ims)
                if ims_time.tzinfo is None:
                    ims_time = ims_time.replace(tzinfo=email.utils.timezone.utc)
                file_time = email.utils.parsedate_to_datetime(last_modified)
                if file_time <= ims_time:
                    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
                    return HTTPResponse('', 304, **headers)
            except Exception:
                pass
        range_header = request.environ.get('HTTP_RANGE')
        if range_header and range_header.startswith('bytes='):
            try:
                ranges = range_header[6:].split(',')[0].strip()
                if '-' not in ranges:
                    raise ValueError
                start_str, end_str = ranges.split('-', 1)
                if start_str == '':
                    start = file_size - int(end_str)
                    end = file_size - 1
                elif end_str == '':
                    start = int(start_str)
                    end = file_size - 1
                else:
                    start = int(start_str)
                    end = int(end_str)
                if start > end or start < 0 or end >= file_size:
                    raise ValueError
                length = end - start + 1
                headers['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                headers['Content-Length'] = str(length)
                if request.method == 'HEAD':
                    body = b''
                else:
                    f = open(abspath, 'rb')
                    f.seek(start)
                    body = f.read(length)
                    f.close()
                return HTTPResponse(body, 206, **headers)
            except Exception:
                return HTTPError(416, 'Requested Range Not Satisfiable')
        if request.method == 'HEAD':
            return HTTPResponse(b'', 200, **headers)
        f = open(abspath, 'rb')
        body = f.read()
        f.close()
        return HTTPResponse(body, 200, **headers)
    except Exception:
        return HTTPError(500, 'Internal Server Error')