```python
def _iter_chunked(read, bufsize):
  while True:
    chunk_line = read(bufsize).rstrip()
    if len(chunk_line) > bufsize or not chunk_line:
      raise HTTPError(400, b"Invalid chunk size")
    try:
      chunk_size = int(chunk_line, 16)
    except ValueError:
      raise HTTPError(400, b"Invalid chunk size")
    if chunk_size == 0:
      return
    data = b''
    while chunk_size > 0:
      chunk = read(min(chunk_size, bufsize))
      if not chunk:
        raise HTTPError(400, b"Missing chunk data")
      data += chunk
      chunk_size -= len(chunk)
    if read(2) != b'\r\n':
      raise HTTPError(400, b"Missing chunk CRLF")
    yield data```