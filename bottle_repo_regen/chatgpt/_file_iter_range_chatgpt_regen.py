# regen 1
def _file_iter_range(fp, chunk_size=65536):
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        yield chunk

# regen 2
def _file_iter_range(fp, chunk_size=65536):
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        yield chunk

# regen 3
def _file_iter_range(fp, chunk_size=65536):
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        yield chunk