```python
def _iter_chunked(read_func, bufsize: int = 102400):
    while True:
        chunk_header = b''
        while True:
            byte = read_func(1)
            if not byte:
                raise ValueError("Unexpected end of stream while reading chunk header")
            chunk_header += byte
            if chunk_header.endswith(b'\r\n'):
                break
            if len(chunk_header) > bufsize:
                raise ValueError("Chunk header exceeds bufsize")
        
        try:
            chunk_length = int(chunk_header.strip().split(b';', 1)[0], 16)
        except ValueError:
            raise ValueError("Invalid hexadecimal chunk length")
        
        if chunk_length == 0:
            break
        
        chunk_data = b''
        while len(chunk_data) < chunk_length:
            data = read_func(chunk_length - len(chunk_data))
            if not data:
                raise ValueError("Unexpected end of stream while reading chunk data")
            chunk_data += data
        
        trailer = read_func(2)
        if trailer != b'\r\n':
            raise ValueError("Invalid chunk trailer")
        
        yield chunk_data
```