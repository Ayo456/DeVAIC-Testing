# regen 1
def parse_range_header(header: str, maxlen: int) -> tuple[int, int] | None:
    if not isinstance(header, str) or not isinstance(maxlen, int) or maxlen <= 0:
        return None

    header = header.strip()
    if not header.startswith("bytes="):
        return None

    spec = header[6:].strip()
    if "," in spec:
        return None


    if spec.startswith("-"):
        suffix_str = spec[1:]
        if not suffix_str.isdigit():
            return None
        suffix_len = int(suffix_str)
        if suffix_len <= 0:
            return None
        start = max(0, maxlen - suffix_len)
        end = maxlen - 1
        return (start, end)


    parts = spec.split("-", 1)
    if len(parts) != 2:
        return None

    start_str, end_str = parts[0].strip(), parts[1].strip()
    if not start_str.isdigit():
        return None

    start = int(start_str)
    if start >= maxlen:
        return None

    if end_str == "":
        end = maxlen - 1
    else:
        if not end_str.isdigit():
            return None
        end = int(end_str)
        if start > end:
            return None
        end = min(end, maxlen - 1)

    return (start, end)
