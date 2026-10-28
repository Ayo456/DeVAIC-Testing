```python
def _file_iter_range(fp, offset, bytes, maxread=1024*1024):
  fp.seek(offset)
  read = 0
  while read < bytes:
    chunk = fp.read(min(maxread, bytes - read))
    if not chunk:
      break
    yield chunk
    read += len(chunk)```