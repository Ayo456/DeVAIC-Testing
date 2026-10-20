def _iter_chunked(read_func, bufsize: int=102400):
    while True:
        line = read_func(bufsize).decode('ascii').strip()
        if not line:
            break
        try:
            chunk_size = int(line, 16)
        except ValueError:
            raise ValueError(f'Invalid chunk size header: {line}')
        if chunk_size == 0:
            break
        chunk = read_func(chunk_size)
        yield chunk