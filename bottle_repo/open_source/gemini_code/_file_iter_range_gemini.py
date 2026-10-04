from typing import BinaryIO, Generator

def _file_iter_range(fp: BinaryIO, chunk_size: int = 65536) -> Generator[bytes, None, None]:
    while True:
        chunk = fp.read(chunk_size)
        if not chunk:
            break
        yield chunk