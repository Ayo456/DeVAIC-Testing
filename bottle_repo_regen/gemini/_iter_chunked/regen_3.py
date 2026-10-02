# regen 3
from typing import Callable, Generator


def _iter_chunked(
    read_func: Callable[[int], bytes], bufsize: int = 102400
) -> Generator[bytes, None, None]:
    """Reads and parses an HTTP chunked transfer encoding stream.

    :param read_func: Callable that accepts an integer number of bytes to read and returns bytes.
    :param bufsize: Maximum allowed header size and buffer size for payload chunks.
    :return: Generator yielding bytes for each chunk.
    :raises ValueError: If the chunk header is invalid, exceeds bufsize, or the stream ends prematurely.
    """
    buffer = bytearray()

    def _read_line() -> bytes:
        nonlocal buffer
        while True:
            newline_idx = buffer.find(b"\n")
            if newline_idx != -1:
                line = buffer[: newline_idx + 1]
                buffer = buffer[newline_idx + 1 :]
                return bytes(line)

            if len(buffer) > bufsize:
                raise ValueError(
                    f"Chunk header exceeds maximum buffer size of {bufsize} bytes"
                )

            chunk = read_func(bufsize)
            if not chunk:
                raise ValueError("Unexpected end of stream while reading chunk header")
            buffer.extend(chunk)

    while True:
        header_line = _read_line()
        if len(header_line) > bufsize:
            raise ValueError(
                f"Chunk header exceeds maximum buffer size of {bufsize} bytes"
            )


        chunk_header = header_line.split(b";", 1)[0].strip()

        try:
            chunk_length = int(chunk_header, 16)
        except ValueError as err:
            raise ValueError(
                f"Invalid chunk length header: {chunk_header!r}"
            ) from err

        if chunk_length < 0:
            raise ValueError(f"Negative chunk length: {chunk_length}")

        if chunk_length == 0:

            while True:
                trailer = _read_line().strip()
                if not trailer:
                    break
            return

        remaining = chunk_length
        while remaining > 0:
            if buffer:
                take = min(len(buffer), remaining)
                segment = bytes(buffer[:take])
                buffer = buffer[take:]
                remaining -= take
                yield segment
            else:
                to_read = min(remaining, bufsize)
                segment = read_func(to_read)
                if not segment:
                    raise ValueError(
                        "Unexpected end of stream while reading chunk payload"
                    )
                remaining -= len(segment)
                yield segment


        while len(buffer) < 2:
            chunk = read_func(bufsize)
            if not chunk:
                raise ValueError(
                    "Unexpected end of stream while reading chunk CRLF"
                )
            buffer.extend(chunk)

        if buffer[:2] == b"\r\n":
            buffer = buffer[2:]
        elif buffer[:1] == b"\n":
            buffer = buffer[1:]
        else:
            raise ValueError("Malformed chunk: missing trailing CRLF")
