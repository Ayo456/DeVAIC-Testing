```python
def parse_range_header(header, maxlen=0):
    if not header or not header.startswith('bytes='):
        return
    for part in header[6:].split(','):
        part = part.strip()
        if '-' not in part:
            continue
        start_str, end_str = part.split('-', 1)
        if start_str:
            try:
                start = int(start_str)
            except ValueError:
                continue
        else:
            start = 0
        if end_str:
            try:
                end = int(end_str) + 1
            except ValueError:
                continue
        else:
            end = maxlen
        if start < 0 or end > maxlen or start >= end:
            continue
        yield (start, min(end, maxlen))
```