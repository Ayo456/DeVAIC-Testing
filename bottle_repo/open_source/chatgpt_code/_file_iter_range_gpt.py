def _file_iter_range(fp, chunk_size=65536):
    while True:
        chunk = fp.read(chunk_size)

        if not chunk:
            break

        yield chunk