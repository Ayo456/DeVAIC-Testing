```python
import os
import mimetypes
import email.utils
import time

def static_file(filename, root, mimetype='auto', download=False, charset='UTF-8'):
    try:
        # Clean filename and resolve path
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
        headers = {
            'Last-Modified': last_modified,
            'Accept-Ranges': 'bytes'
        }
        # Guess mimetype and encoding
        guessed_type, guessed_enc = (None, None)
        if mimetype == 'auto':
            guessed_type, guessed_enc = mimetypes.guess_type(abspath)
            ctype = guessed_type or 'application/octet-stream'
            if guessed_enc:
                headers['Content-Encoding'] = guessed_enc
        else:
            ctype = mimetype
        # Add charset for text/*
        if ctype.startswith('text/') and 'charset=' not in ctype and charset:
            ctype += f'; charset={charset}'
        headers['Content-Type'] = ctype
        # Content-Disposition
        if download:
            if isinstance(download, str):
                disp_name = os.path.basename(download)
            else:
                disp_name = os.path.basename(abspath)
            headers['Content-Disposition'] = f'attachment; filename="{disp_name}"'
        # If-Modified-Since
        ims = request.environ.get('HTTP_IF_MODIFIED_SINCE')
        if ims:
            try:
                ims_time = email.utils.parsedate_to_datetime(ims)
                if ims_time.tzinfo is None:
                    ims_time = ims_time.replace(tzinfo=email.utils.localtime().tzinfo)
                if mtime <= ims_time.timestamp():
                    headers['Date'] = email.utils.formatdate(time.time(), usegmt=True)
                    return HTTPResponse('', 304, **headers)
            except Exception:
                pass
        # Range support
        range_header = request.environ.get('HTTP_RANGE')
        status = 200
        body = None
        if range_header:
            try:
                units, rng = range_header.strip().split('=', 1)
                if units != 'bytes':
                    raise ValueError
                ranges = rng.split(',')[0].strip()
                if '-' not in ranges:
                    raise ValueError
                start_s, end_s = ranges.split('-', 1)
                if start_s == '':
                    # suffix-byte-range-spec: last N bytes
                    start = file_size - int(end_s)
                    end = file_size - 1
                elif end_s == '':
                    start = int(start_s)
                    end = file_size - 1
                else:
                    start = int(start_s)
                    end = int(end_s)
                if start < 0 or end < start or end >= file_size:
                    raise ValueError
                length = end - start + 1
                headers['Content-Range'] = f'bytes {start}-{end}/{file_size}'
                headers['Content-Length'] = str(length)
                status = 206
                if request.method == 'HEAD':
                    body = b''
                else:
                    f = open(abspath, 'rb')
                    f.seek(start)
                    body = f.read(length)
                    f.close()
            except Exception:
                return HTTPError(416, 'Requested Range Not Satisfiable')
        else:
            headers['Content-Length'] = str(file_size)
            if request.method == 'HEAD':
                body = b''
            else:
                body = open(abspath, 'rb')
        return HTTPResponse(body, status, **headers)
    except Exception:
        return HTTPError(500, 'Internal Server Error')
```