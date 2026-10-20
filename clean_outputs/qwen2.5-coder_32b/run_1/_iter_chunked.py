def _iter_chunked(read_func, bufsize: int=102400):
    while True:
        chunk_header = b''
        while True:
            byte = read_func(1)
            if not byte:
                raise ValueError('Unexpected end of stream while reading chunk header')
            chunk_header += byte
            if b'\r\n' in chunk_header:
                break
            if len(chunk_header) > bufsize:
                raise ValueError('Chunk header exceeds maximum buffer size')
        chunk_length_str, _ = chunk_header.split(b'\r\n', 1)
        try:
            chunk_length = int(chunk_length_str, 16)
        except ValueError:
            raise ValueError('Invalid hexadecimal chunk length')
        if chunk_length == 0:
            break
        chunk_data = b''
        while len(chunk_data) < chunk_length:
            data = read_func(chunk_length - len(chunk_data))
            if not data:
                raise ValueError('Unexpected end of stream while reading chunk data')
            chunk_data += data
        trailer = read_func(2)
        if trailer != b'\r\n':
            raise ValueError('Invalid chunk trailer')
        yield chunk_data