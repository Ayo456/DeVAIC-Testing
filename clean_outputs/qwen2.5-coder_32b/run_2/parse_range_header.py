def parse_range_header(header: str, maxlen: int):
    if not header.startswith('bytes='):
        return None
    range_part = header[6:]
    parts = range_part.split('-')
    if len(parts) != 2:
        return None
    start_str, end_str = parts
    try:
        if start_str:
            start = int(start_str)
        else:
            start = None
        if end_str:
            end = int(end_str)
        else:
            end = None
    except ValueError:
        return None
    if start is not None and end is not None:
        if start < 0 or end >= maxlen or start > end:
            return None
        return (start, end)
    elif start is not None:
        if start < 0 or start >= maxlen:
            return None
        return (start, maxlen - 1)
    elif end is not None:
        if end < 0 or end >= maxlen:
            return None
        start = maxlen - end - 1
        if start < 0:
            return None
        return (start, maxlen - 1)
    else:
        return None