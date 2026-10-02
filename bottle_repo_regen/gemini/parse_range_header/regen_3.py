# regen 3
from typing import Optional, Tuple


def parse_range_header(header: str, maxlen: int) -> Optional[Tuple[int, int]]:
    """
    Parses an HTTP Range header string (e.g. 'bytes=0-499') against a total resource length maxlen.
    Returns (start, end) as inclusive byte boundaries, or None if invalid or unsatisfiable.
    """
    if not isinstance(header, str) or maxlen <= 0:
        return None

    header = header.strip()
    prefix = "bytes="
    if not header.startswith(prefix):
        return None

    range_spec = header[len(prefix) :].strip()


    if "," in range_spec:
        return None

    parts = range_spec.split("-", 1)
    if len(parts) != 2:
        return None

    first_str, last_str = parts[0].strip(), parts[1].strip()


    if first_str == "":
        if not last_str.isdigit():
            return None
        suffix_len = int(last_str)
        if suffix_len == 0:
            return None
        start = max(0, maxlen - suffix_len)
        end = maxlen - 1
        return (start, end)


    if not first_str.isdigit():
        return None

    start = int(first_str)

    if last_str == "":
        end = maxlen - 1
    else:
        if not last_str.isdigit():
            return None
        end = int(last_str)


    if start > end or start >= maxlen:
        return None

    end = min(end, maxlen - 1)
    return (start, end)
