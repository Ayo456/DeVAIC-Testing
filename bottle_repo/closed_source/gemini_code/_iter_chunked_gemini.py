from typing import Callable, Generator

def _iter_chunked(read_func: Callable[[int], bytes], bufsize: int = 102400) -> Generator[bytes, None, None]:
    buffer = b""

    def read_line() -> bytes:
        nonlocal buffer
        while b"\r\n" not in buffer:
            if len(buffer) > bufsize:
                raise ValueError("Chunk header exceeds buffer size")
            chunk = read_func(bufsize)
            if not chunk:
                raise IOError("Unexpected end of stream while reading chunk header")
            buffer += chunk

        line, buffer = buffer.split(b"\r\n", 1)
        if len(line) > bufsize:
            raise ValueError("Chunk header exceeds buffer size")
        return line

    def read_exact(n: int) -> bytes:
        nonlocal buffer
        chunks = []
        needed = n
        if buffer:
            take = min(len(buffer), needed)
            chunks.append(buffer[:take])
            buffer = buffer[take:]
            needed -= take

        while needed > 0:
            chunk = read_func(min(needed, bufsize))
            if not chunk:
                raise IOError("Unexpected end of stream while reading chunk data")
            chunks.append(chunk)
            needed -= len(chunk)

        return b"".join(chunks)

    while True:
        header_line = read_line()
        chunk_spec = header_line.split(b";", 1)[0].strip()

        try:
            chunk_length = int(chunk_spec, 16)
        except ValueError:
            raise ValueError(f"Invalid hexadecimal chunk size: {chunk_spec!r}")

        if chunk_length < 0:
            raise ValueError(f"Negative chunk length: {chunk_length}")

        if chunk_length == 0:
            while True:
                trailer = read_line()
                if not trailer:
                    break
            return

        remaining = chunk_length
        while remaining > 0:
            to_read = min(remaining, bufsize)
            data = read_exact(to_read)
            remaining -= len(data)
            yield data

        crlf = read_exact(2)
        if crlf != b"\r\n":
            raise ValueError("Malformed chunk: missing trailing CRLF")