# regen 2
def _iter_chunked(read_func, bufsize: int = 102400):
    while True:
        header = bytearray()

        while not header.endswith(b"\n"):
            if len(header) >= bufsize:
                raise ValueError("Chunk header exceeds bufsize")

            data = read_func(1)

            if not data:
                raise EOFError("Unexpected end of stream while reading chunk header")

            header.extend(data)

        header = bytes(header).strip()

        try:
            chunk_size = int(header.split(b";", 1)[0], 16)
        except ValueError:
            raise ValueError("Invalid hexadecimal chunk header")

        if chunk_size == 0:
            return

        remaining = chunk_size

        while remaining > 0:
            data = read_func(min(remaining, bufsize))

            if not data:
                raise EOFError("Unexpected end of stream while reading chunk data")

            yield data
            remaining -= len(data)

        ending = read_func(2)

        if ending != b"\r\n":
            raise ValueError("Invalid chunk terminator")
