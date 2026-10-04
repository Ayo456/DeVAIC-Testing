def _iter_chunked(read_func, bufsize: int=102400):

    def read_line():
        line = bytearray()
        while True:
            byte = read_func(1)
            if not byte:
                break
            line.append(byte[0])
            if line.endswith(b'\r\n'):
                break
            if len(line) > bufsize:
                raise ValueError('Chunk header exceeds bufsize')
        return line
    while True:
        chunk_length_line = read_line()
        if not chunk_length_line:
            raise ValueError('Unexpected end of stream while reading chunk length')
        try:
            chunk_length_str = chunk_length_line.decode('ascii').split(';', 1)[0].strip()
            chunk_length = int(chunk_length_str, 16)
        except ValueError:
            raise ValueError(f'Invalid chunk length header: {chunk_length_line}')
        if chunk_length == 0:
            while read_line().strip():
                pass
            break
        chunk_data = bytearray()
        while len(chunk_data) < chunk_length:
            data = read_func(chunk_length - len(chunk_data))
            if not data:
                raise ValueError('Unexpected end of stream while reading chunk data')
            chunk_data.extend(data)
        crlf = read_func(2)
        if crlf != b'\r\n':
            raise ValueError('Expected CRLF after chunk data')
        yield chunk_data