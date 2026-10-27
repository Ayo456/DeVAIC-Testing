def _iter_chunked(read, bufsize):
    import re
    CRLF = b'\r\n'
    CHUNK_SIZE_LINE_RE = re.compile(b'^([0-9A-Fa-f]+)')

    def read_line():
        line = bytearray()
        while True:
            if len(line) > bufsize:
                raise HTTPError(400, b'Bad Request')
            c = read(1)
            if not c:
                raise HTTPError(400, b'Bad Request')
            line += c
            if line[-2:] == CRLF:
                return bytes(line[:-2])
    while True:
        line = read_line()
        if len(line) > bufsize:
            raise HTTPError(400, b'Bad Request')
        m = CHUNK_SIZE_LINE_RE.match(line.split(b';', 1)[0])
        if not m:
            raise HTTPError(400, b'Bad Request')
        try:
            size = int(m.group(1), 16)
        except ValueError:
            raise HTTPError(400, b'Bad Request')
        if size == 0:
            break
        remaining = size
        while remaining > 0:
            to_read = min(remaining, bufsize)
            data = read(to_read)
            if not data:
                raise HTTPError(400, b'Bad Request')
            yield data
            remaining -= len(data)
        crlf = b''
        while len(crlf) < 2:
            more = read(2 - len(crlf))
            if not more:
                raise HTTPError(400, b'Bad Request')
            crlf += more
        if crlf != CRLF:
            raise HTTPError(400, b'Bad Request')