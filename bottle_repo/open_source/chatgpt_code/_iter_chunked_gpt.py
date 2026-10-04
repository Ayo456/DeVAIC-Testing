def _iter_chunked(read_func, bufsize: int = 102400):
    def read_line():
        line = bytearray()

        while True:
            if len(line) >= bufsize:
                raise OverflowError("Chunk header exceeds buffer size")

            byte = read_func(1)

            if not byte:
                raise EOFError("Unexpected end of chunked stream")

            line.extend(byte)

            if line.endswith(b"\r\n"):
                return bytes(line[:-2])

    def read_exact(size):
        remaining = size

        while remaining:
            data = read_func(min(remaining, bufsize))

            if not data:
                raise EOFError("Unexpected end of chunked stream")

            remaining -= len(data)
            yield data

    while True:
        header = read_line()
        size_text = header.split(b";", 1)[0].strip()

        if not size_text:
            raise ValueError("Invalid chunk header")

        if any(c not in b"0123456789abcdefABCDEF" for c in size_text):
            raise ValueError("Invalid hexadecimal chunk size")

        size = int(size_text, 16)

        if size == 0:
            return

        yield from read_exact(size)

        if read_func(2) != b"\r\n":
            raise ValueError("Invalid chunk terminator")