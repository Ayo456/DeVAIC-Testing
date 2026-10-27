```python
def _file_iter_range(fp, offset, bytes, maxread=1024*1024):
    fp.seek(offset)
    remaining = bytes
    while remaining > 0:
        to_read = min(remaining, maxread)
        chunk = fp.read(to_read)
        if not chunk:
            break
        yield chunk
        remaining -= len(chunk)
```