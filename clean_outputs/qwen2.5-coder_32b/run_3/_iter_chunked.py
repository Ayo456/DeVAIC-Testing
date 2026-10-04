def _iter_chunked(read_func, bufsize: int=102400):

    def read_line():
        line = bytearray()
        while True:
            byte = read_func(1)
            if not byte:
                break
            line.append(byte[0])
            if len(line) > bufsize:
                raise ValueError('Chunk header exceeds buffer size.')
            if byte == b'\n':
                break
        return bytes(line)

    def parse_chunk_length(header):
        try:
            end_pos = header.find(b' ')
            if end_pos == -1:
                end_pos = header.find(b'\r')
            if end_pos == -1:
                end_pos = header.find(b'\n')
            if end_pos == -1:
                end_pos = len(header)
            chunk_length = int(header[:end_pos], 16)
        except ValueError:
            raise ValueError('Invalid hexadecimal characters in chunk header.')
        return chunk_length
    while True:
        header_line = read_line()
        if not header_line:
            break
        chunk_length = parse_chunk_length(header_line)
        if chunk_length == 0:
            break
        chunk_data = bytearray()
        while len(chunk_data) < chunk_length:
            data = read_func(chunk_length - len(chunk_data))
            if not data:
                raise ValueError('Premature end of chunked data.')
            chunk_data.extend(data)
        trailing_crlf = read_func(2)
        if trailing_crlf != b'\r\n':
            raise ValueError('Invalid trailing CRLF after chunk data.')
        yield bytes(chunk_data)