```python
def _iter_chunked(read, bufsize):
  while True:
    chunk_size_line = read(bufsize).strip()
    if not chunk_size_line:
      break
    try:
      chunk_size = int(chunk_size_line, 16)
    except ValueError:
      raise HTTPError(400, b"Invalid chunk size")
    if chunk_size == 0:
      break
    chunk_data = b''
    while len(chunk_data) < chunk_size:
      chunk_data += read(bufsize)
      if not chunk_data:
        raise HTTPError(400, b"Incomplete chunk")
    if len(chunk_data) > chunk_size:
      raise HTTPError(400, b"Chunk size exceeded")
    yield chunk_data
    if read(2) != b'\r\n':
      raise HTTPError(400, b"Missing CRLF after chunk")```