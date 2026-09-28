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

# regen 3
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

        while not header.endswith(b"\r\n"):
            if len(header) >= bufsize:
                raise ValueError("Chunk header exceeds bufsize")

            byte = read_func(1)

            if not byte:
                raise EOFError("Unexpected end of chunk header")

            header.extend(byte)

        chunk_header = header[:-2]

        if not chunk_header:
            raise ValueError("Empty chunk header")

        try:
            chunk_size = int(chunk_header, 16)
        except ValueError:
            raise ValueError("Invalid hexadecimal chunk header")

        if chunk_size == 0:
            return

        remaining = chunk_size

        while remaining > 0:
            amount = min(remaining, bufsize)
            data = read_exact(amount)
            yield data
            remaining -= len(data)

        if read_exact(2) != b"\r\n":
            raise ValueError("Invalid chunk terminator")