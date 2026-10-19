from typing import Optional, Tuple

def parse_range_header(header: str, maxlen: int) -> Optional[Tuple[int, int]]:
    if not isinstance(header, str) or not isinstance(maxlen, int) or maxlen <= 0:
        return None

    header = header.strip()
    if not header.startswith("bytes="):
        return None

    ranges = header[6:].split(",")
    if len(ranges) != 1:
        return None

    byte_range = ranges[0].strip()
    if "-" not in byte_range:
        return None

    first, last = byte_range.split("-", 1)

    if not first and not last:
        return None

    if not first:
        try:
            suffix_length = int(last)
        except ValueError:
            return None
        if suffix_length <= 0:
            return None
        start = max(0, maxlen - suffix_length)
        end = maxlen - 1
        return start, end

    try:
        start = int(first)
    except ValueError:
        return None

    if not last:
        end = maxlen - 1
    else:
        try:
            end = int(last)
        except ValueError:
            return None

    if start < 0 or end < start or start >= maxlen:
        return None

    end = min(end, maxlen - 1)
    return start, end