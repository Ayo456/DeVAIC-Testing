def parse_range_header(header: str, maxlen: int):
    if not header.startswith('bytes='):
        return None
    range_spec = header[6:]
    parts = range_spec.split('-')
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
    if start is None and end is None:
        return None
    if start is None and end is not None:
        if end > maxlen:
            return None
        start = maxlen - end
        end = maxlen - 1
    if start is not None and end is None:
        if start >= maxlen:
            return None
        end = maxlen - 1
    if start is not None and end is not None:
        if start >= maxlen or end >= maxlen or start > end:
            return None
    return (start, end)