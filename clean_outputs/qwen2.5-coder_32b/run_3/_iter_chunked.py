def _iter_chunked(read, bufsize):
    while True:
        size_line = b''
        while len(size_line) < bufsize:
            chunk = read(bufsize - len(size_line))
            if not chunk:
                raise HTTPError(400, b'Bad Request')
            size_line += chunk
            if b'\r\n' in size_line:
                break
        else:
            raise HTTPError(400, b'Bad Request')
        size_str, _, _ = size_line.split(b';', 1) if b';' in size_line else (size_line, b'', b'')
        try:
            size = int(size_str.strip(), 16)
        except ValueError:
            raise HTTPError(400, b'Bad Request')
        if size == 0:
            if read(2) != b'\r\n':
                raise HTTPError(400, b'Bad Request')
            return
        while size > 0:
            chunk = read(min(size, bufsize))
            if not chunk:
                raise HTTPError(400, b'Bad Request')
            yield chunk
            size -= len(chunk)
        if read(2) != b'\r\n':
            raise HTTPError(400, b'Bad Request')