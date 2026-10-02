# regen 1
def _iter_chunked(read_func, bufsize: int = 102400):
    def read_exact(size):
        data = bytearray()

        while len(data) < size:
            chunk = read_func(size - len(data))

            if not chunk:
                raise EOFError("Unexpected end of chunked stream")

            data.extend(chunk)

        return bytes(data)

    while True:
        header = bytearray()

        while True:
            byte = read_func(1)

            if not byte:
                raise EOFError("Unexpected end of stream while reading chunk header")

            header.extend(byte)

            if len(header) > bufsize:
                raise ValueError("Chunk header exceeds bufsize")

            if header.endswith(b"\r\n"):
                break

        header = header[:-2]

        if not header:
            raise ValueError("Empty chunk header")

        try:
            chunk_size = int(header, 16)
        except ValueError:
            raise ValueError("Invalid hexadecimal chunk header")

        if chunk_size == 0:
            return

        remaining = chunk_size

        while remaining > 0:
            size = min(remaining, bufsize)
            data = read_exact(size)
            yield data
            remaining -= len(data)

        if read_exact(2) != b"\r\n":
            raise ValueError("Invalid chunk terminator")
