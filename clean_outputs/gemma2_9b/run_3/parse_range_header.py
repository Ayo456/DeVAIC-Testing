def parse_range_header(header: str, maxlen: int) -> tuple[int, int] | None:
    try:
        _, start_end = header.split('=')
        start, end = map(int, start_end.split('-'))
    except ValueError:
        return None
    if start < 0:
        return None
    if end >= maxlen:
        return None
    if end < start:
        return None
    return (start, end)