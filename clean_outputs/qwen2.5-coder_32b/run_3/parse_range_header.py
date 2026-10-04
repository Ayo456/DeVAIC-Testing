def parse_range_header(header: str, maxlen: int) -> tuple:
    if not header.startswith('bytes='):
        return None
    range_spec = header[6:]
    parts = range_spec.split('-')
    if len(parts) != 2:
        return None
    start_str, end_str = parts
    if start_str == '' and end_str == '':
        return None
    try:
        if start_str == '':
            start = maxlen - int(end_str)
            end = maxlen - 1
        elif end_str == '':
            start = int(start_str)
            end = maxlen - 1
        else:
            start = int(start_str)
            end = int(end_str)
    except ValueError:
        return None
    if start < 0 or end >= maxlen or start > end:
        return None
    return (start, end)
print(parse_range_header('bytes=0-499', 1000))
print(parse_range_header('bytes=500-', 1000))
print(parse_range_header('bytes=-500', 1000))
print(parse_range_header('bytes=1000-2000', 1000))
print(parse_range_header('bytes=-1000', 1000))
print(parse_range_header('bytes=1000-999', 1000))
print(parse_range_header('bytes=abc-499', 1000))