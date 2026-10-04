def parse_range_header(header: str, maxlen: int) -> tuple[int, int] | None:
    try:
        start, end = map(int, header.split('-'))
    except ValueError:
        return None
    if start < 0:
        return None
    if end >= maxlen:
        end = maxlen - 1
    return (start, end)