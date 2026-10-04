def _iter_chunked(read_func, bufsize: int=102400) -> iter[bytes]:
    while True:
        chunk_header = read_func()
        if not chunk_header:
            break
        try:
            chunk_size = int(chunk_header.strip(), 16)
        except ValueError:
            raise ValueError('Invalid hexadecimal chunk size in header: {}'.format(chunk_header))
        if chunk_size > bufsize:
            raise ValueError('Chunk size exceeds maximum allowed size: {}'.format(chunk_size))
        chunk_data = read_func()
        if len(chunk_data) != chunk_size:
            raise ValueError('Chunk data length does not match header size.')
        yield chunk_data
        if chunk_size == 0:
            break