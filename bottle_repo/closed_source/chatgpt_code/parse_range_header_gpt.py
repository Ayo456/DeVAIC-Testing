def parse_range_header(header: str, maxlen: int):
    if not isinstance(header, str) or not isinstance(maxlen, int) or maxlen <= 0:
        return None

    if not header.startswith("bytes="):
        return None

    value = header[6:].strip()

    if "," in value or "-" not in value:
        return None

    start_str, end_str = value.split("-", 1)

    try:
        if not start_str:
            length = int(end_str)

            if length <= 0:
                return None

            length = min(length, maxlen)
            return maxlen - length, maxlen - 1

        start = int(start_str)

        if start < 0 or start >= maxlen:
            return None

        if not end_str:
            return start, maxlen - 1

        end = int(end_str)

        if end < start or end >= maxlen:
            return None

        return start, end

    except ValueError:
        return None