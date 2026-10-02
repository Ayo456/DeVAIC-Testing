# regen 1
from typing import Callable, Generator


def _iter_chunked(
    read_func: Callable[[int], bytes], bufsize: int = 102400
) -> Generator[bytes, None, None]:
    buffer = bytearray()

    def _read_line() -> bytes:
        while True:
            nl_idx = buffer.find(b"\n")
            if nl_idx != -1:
                line = bytes(buffer[: nl_idx + 1])
                del buffer[: nl_idx + 1]
                return line
            if len(buffer) > bufsize:
                raise ValueError("Chunk header exceeds maximum buffer size")
            chunk = read_func(bufsize)
            if not chunk:
                raise ValueError("Premature end of stream while reading chunk header")
            buffer.extend(chunk)

    def _read_exact(n: int) -> bytes:
        nonlocal buffer
        while len(buffer) < n:
            chunk = read_func(bufsize)
            if not chunk:
                raise ValueError("Premature end of stream while reading chunk data")
            buffer.extend(chunk)
        data = bytes(buffer[:n])
        del buffer[:n]
        return data

    while True:
        header_line = _read_line()
        if len(header_line) > bufsize:
            raise ValueError("Chunk header exceeds maximum buffer size")


        header_str = header_line.decode("latin1").strip("\r\n")
        chunk_len_str = header_str.split(";", 1)[0].strip()

        if not chunk_len_str:
            raise ValueError("Empty chunk header encountered")

        try:
            chunk_length = int(chunk_len_str, 16)
        except ValueError as err:
            raise ValueError(
                f"Invalid hexadecimal chunk header: {chunk_len_str!r}"
            ) from err

        if chunk_length < 0:
            raise ValueError(f"Negative chunk length: {chunk_length}")

        if chunk_length == 0:

            while True:
                trailer_line = _read_line()
                if trailer_line in (b"\r\n", b"\n"):
                    break
            return


        bytes_left = chunk_length
        while bytes_left > 0:
            to_read = min(bytes_left, bufsize)
            if not buffer:
                chunk_data = read_func(to_read)
                if not chunk_data:
                    raise ValueError("Premature end of stream in chunk body")
            else:
                take = min(len(buffer), to_read)
                chunk_data = bytes(buffer[:take])
                del buffer[:take]

            bytes_left -= len(chunk_data)
            yield chunk_data


        crlf = _read_exact(2)
        if crlf not in (b"\r\n", b"\n\r"):
            if crlf.startswith(b"\n"):
                buffer = bytearray(crlf[1:]) + buffer
            else:
                raise ValueError("Malformed chunk terminator: expected CRLF")
