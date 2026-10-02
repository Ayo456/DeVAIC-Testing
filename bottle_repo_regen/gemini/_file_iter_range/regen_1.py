# regen 1
def _file_iter_range(fp, chunk_size=65536):
    while chunk := fp.read(chunk_size):
        yield chunk
