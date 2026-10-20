```python
def parse_range_header(header: str, maxlen: int):
    if not header.startswith('bytes='):
        return None
    try:
        range_spec = header[6:].split('-')
        if len(range_spec) != 2:
            return None
        start = int(range_spec[0]) if range_spec[0] else None
        end = int(range_spec[1]) if range_spec[1] else None
        if start is None and end is None:
            return None
        if start is not None and (start < 0 or start >= maxlen):
            return None
        if end is not None and (end < 0 or end >= maxlen):
            return None
        if start is not None and end is not None and start > end:
            return None
        if start is None:
            start = maxlen - (end + 1)
            end = maxlen - 1
        elif end is None:
            end = maxlen - 1
        return (start, end)
    except ValueError:
        return None
```