def parse_range_header(header: str, maxlen: int) -> tuple[int, int] | None:
    if not header.startswith('bytes='):
        return None
    try:
        start, end = map(int, header[6:].split('-'))
    except ValueError:
        return None
    if start < 0 or end >= maxlen or start > end:
        return None
    return (start, end)