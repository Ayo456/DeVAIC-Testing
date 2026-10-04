def _iter_chunked(read_func, bufsize: int=102400) -> bytes:
    while True:
        chunk_header = read_func(bufsize).decode('ascii').strip()
        if not chunk_header:
            break
        try:
            chunk_size = int(chunk_header, 16)
        except ValueError:
            raise ValueError(f'Invalid chunk size: {chunk_header}')
        if chunk_size == 0:
            break
        chunk_data = read_func(chunk_size)
        yield chunk_data
        read_func(2)