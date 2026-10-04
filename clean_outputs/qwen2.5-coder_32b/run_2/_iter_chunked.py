def _iter_chunked(read_func, bufsize: int=102400):

    def read_until_newline():
        buffer = bytearray()
        while True:
            char = read_func(1)
            if not char:
                break
            buffer.extend(char)
            if buffer.endswith(b'\r\n'):
                return buffer[:-2]
        raise ValueError('Unexpected end of stream while reading chunk header')
    while True:
        header = read_until_newline()
        if len(header) > bufsize:
            raise ValueError(f'Chunk header exceeds buffer size of {bufsize} bytes')
        try:
            chunk_length = int(header, 16)
        except ValueError:
            raise ValueError(f'Invalid hexadecimal chunk length: {header}')
        if chunk_length == 0:
            trailer = read_func(2)
            if trailer != b'\r\n':
                raise ValueError(f'Expected CRLF after zero-length chunk, got: {trailer}')
            break
        chunk_data = bytearray()
        while len(chunk_data) < chunk_length:
            data = read_func(chunk_length - len(chunk_data))
            if not data:
                raise ValueError('Unexpected end of stream while reading chunk data')
            chunk_data.extend(data)
        crlf = read_func(2)
        if crlf != b'\r\n':
            raise ValueError(f'Expected CRLF at the end of chunk, got: {crlf}')
        yield bytes(chunk_data)