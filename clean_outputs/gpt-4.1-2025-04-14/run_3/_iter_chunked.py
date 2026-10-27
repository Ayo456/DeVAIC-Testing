def _iter_chunked(read, bufsize):
    import re
    CRLF = b'\r\n'

    class HTTPError(Exception):

        def __init__(self, status, body):
            super().__init__(f'{status} {body}')
            self.status = status
            self.body = body

    def read_line():
        line = bytearray()
        while True:
            if len(line) > bufsize:
                raise HTTPError(400, b'Bad Request')
            chunk = read(1)
            if not chunk:
                raise HTTPError(400, b'Bad Request')
            line += chunk
            if line[-2:] == CRLF:
                return bytes(line[:-2])
    while True:
        size_line = bytearray()
        while True:
            if len(size_line) > bufsize:
                raise HTTPError(400, b'Bad Request')
            b = read(1)
            if not b:
                raise HTTPError(400, b'Bad Request')
            size_line += b
            if size_line[-2:] == CRLF:
                break
        size_line = bytes(size_line[:-2])
        if b';' in size_line:
            size_line = size_line.split(b';', 1)[0]
        size_line = size_line.strip()
        try:
            chunk_size = int(size_line, 16)
        except Exception:
            raise HTTPError(400, b'Bad Request')
        if chunk_size == 0:
            trailer = bytearray()
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
                    return
            return
        remaining = chunk_size
        while remaining > 0:
            to_read = min(remaining, bufsize)
            data = read(to_read)
            if not data:
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