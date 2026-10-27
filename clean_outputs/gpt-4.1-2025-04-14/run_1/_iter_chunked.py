def _iter_chunked(read, bufsize):
    import re
    CRLF = b'\r\n'
    HEXDIGITS = b'0123456789abcdefABCDEF'

    def read_line():
        line = bytearray()
        while True:
            if len(line) > bufsize:
                raise HTTPError(400, b'Bad Request')
            b = read(1)
            if not b:
                raise HTTPError(400, b'Bad Request')
            line += b
            if line[-2:] == CRLF:
                return bytes(line[:-2])
    while True:
        line = read_line()
        if len(line) > bufsize:
            raise HTTPError(400, b'Bad Request')
        semi = line.find(b';')
        if semi != -1:
            size_str = line[:semi]
        else:
            size_str = line
        size_str = size_str.strip()
        if not size_str or any((c not in HEXDIGITS for c in size_str)):
            raise HTTPError(400, b'Bad Request')
        try:
            size = int(size_str, 16)
        except ValueError:
            raise HTTPError(400, b'Bad Request')
        if size == 0:
            while True:
                trailer = bytearray()
                while True:
                    if len(trailer) > bufsize:
                        raise HTTPError(400, b'Bad Request')
                    b = read(1)
                    if not b:
                        raise HTTPError(400, b'Bad Request')
                    trailer += b
                    if trailer[-2:] == CRLF:
                        break
                if len(trailer) == 2:
                    break
            return
        remaining = size
        while remaining > 0:
            to_read = min(remaining, bufsize)
            data = read(to_read)
            if not data or len(data) == 0:
                raise HTTPError(400, b'Bad Request')
            yield data
            remaining -= len(data)
        crlf = b''
        while len(crlf) < 2:
            b = read(2 - len(crlf))
            if not b:
                raise HTTPError(400, b'Bad Request')
            crlf += b
        if crlf != CRLF:
            raise HTTPError(400, b'Bad Request')