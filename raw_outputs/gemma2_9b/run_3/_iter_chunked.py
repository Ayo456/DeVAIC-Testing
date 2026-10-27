```python
def _iter_chunked(read, bufsize):
  while True:
    chunk_line = read(bufsize).rstrip()
    if not chunk_line:
      break
    try:
      size = int(chunk_line.split(';')[0], 16)
    except ValueError:
      raise HTTPError(400, b"Invalid chunk size")
    if size == 0:
      break
    data = b''
    while len(data) < size:
      chunk = read(bufsize)
      if not chunk:
        raise HTTPError(400, b"Missing chunk data")
      data += chunk
    if data[-2:] != b'\r\n':
      raise HTTPError(400, b"Missing chunk CRLF")
    yield data[:size]
```