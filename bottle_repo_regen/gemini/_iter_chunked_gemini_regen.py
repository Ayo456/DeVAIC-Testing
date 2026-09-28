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

# regen 2
from typing import Callable, Generator


class ChunkedEncodingError(Exception):
    """Raised when parsing invalid chunked transfer encoding data."""


def _iter_chunked(
    read_func: Callable[[int], bytes], bufsize: int = 102400
) -> Generator[bytes, None, None]:
    """Reads and parses an HTTP chunked transfer encoding stream.

    Args:
        read_func: Callback taking an integer byte count and returning bytes.
        bufsize: Maximum allowed size for buffering chunk headers/lines.

    Yields:
        Byte segments corresponding to each chunk payload.

    Raises:
        ChunkedEncodingError: If a header exceeds bufsize, chunk-size is invalid hex,
                              CRLF delimiters are missing, or EOF is encountered prematurely.
    """
    buffer = bytearray()

    def _read_exact(n: int) -> bytes:
        data = bytearray()
        while len(data) < n:
            chunk = read_func(n - len(data))
            if not chunk:
                raise ChunkedEncodingError(
                    f"Unexpected EOF while reading {n} bytes (got {len(data)})"
                )
            data.extend(chunk)
        return bytes(data)

    def _readline() -> bytes:
        while True:
            newline_idx = buffer.find(b"\n")
            if newline_idx != -1:
                line = bytes(buffer[: newline_idx + 1])
                del buffer[: newline_idx + 1]
                return line

            if len(buffer) >= bufsize:
                raise ChunkedEncodingError(
                    f"Chunk header exceeds maximum buffer size of {bufsize} bytes"
                )

            chunk = read_func(min(bufsize - len(buffer), 4096))
            if not chunk:
                raise ChunkedEncodingError("Unexpected EOF while reading chunk header")
            buffer.extend(chunk)

    while True:

        header_line = _readline().rstrip(b"\r\n")


        size_token = header_line.split(b";", 1)[0].strip()

        try:
            chunk_length = int(size_token, 16)
        except (ValueError, TypeError):
            raise ChunkedEncodingError(f"Invalid hexadecimal chunk size: {size_token!r}")

        if chunk_length < 0:
            raise ChunkedEncodingError(f"Negative chunk length: {chunk_length}")

        if chunk_length == 0:

            while True:
                trailer = _readline()
                if trailer in (b"\r\n", b"\n"):
                    break
            return


        bytes_remaining = chunk_length
        while bytes_remaining > 0:
            if buffer:
                take = min(len(buffer), bytes_remaining)
                data = bytes(buffer[:take])
                del buffer[:take]
            else:
                data = read_func(min(bytes_remaining, bufsize))
                if not data:
                    raise ChunkedEncodingError(
                        f"Unexpected EOF inside chunk payload ({bytes_remaining} bytes remaining)"
                    )
            bytes_remaining -= len(data)
            yield data


        if len(buffer) >= 2:
            crlf = bytes(buffer[:2])
            del buffer[:2]
        else:
            needed = 2 - len(buffer)
            crlf = bytes(buffer) + _read_exact(needed)
            buffer.clear()

        if crlf not in (b"\r\n", b"\n\r"):
            if crlf.startswith(b"\n"):

                buffer.extend(crlf[1:])
            else:
                raise ChunkedEncodingError(f"Malformed chunk delimiter: {crlf!r}")

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

