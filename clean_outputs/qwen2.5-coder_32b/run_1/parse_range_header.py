def parse_range_header(header: str, maxlen: int):
    if not header.startswith('bytes='):
        return None
    try:
        range_spec = header.split('=')[1]
        start, end = range_spec.split('-')
        start = int(start) if start else 0
        end = int(end) if end else maxlen - 1
        if start < 0 or end >= maxlen or start > end:
            return None
        return (start, end)
    except (ValueError, IndexError):
        return None