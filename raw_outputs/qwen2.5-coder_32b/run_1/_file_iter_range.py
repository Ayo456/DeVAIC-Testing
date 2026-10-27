```python
def _file_iter_range(fp, offset, bytes, maxread=1024*1024):
    fp.seek(offset)
    remaining = bytes
    while remaining > 0:
        chunk_size = min(remaining, maxread)
        data = fp.read(chunk_size)
        if not data:
            break
        yield data
        remaining -= len(data)
```