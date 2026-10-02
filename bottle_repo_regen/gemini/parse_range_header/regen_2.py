# regen 2
from typing import Optional, Tuple


def parse_range_header(header: str, maxlen: int) -> Optional[Tuple[int, int]]:
    if not isinstance(header, str) or maxlen <= 0:
        return None

    header = header.strip()
    prefix = "bytes="
    if not header.startswith(prefix):
        return None

    range_spec = header[len(prefix) :].strip()


    if "," in range_spec:
        return None

    parts = range_spec.split("-")
    if len(parts) != 2:
        return None

    start_str, end_str = parts[0].strip(), parts[1].strip()


    if start_str == "":
        if not end_str.isdigit():
            return None
        suffix_len = int(end_str)
        if suffix_len == 0:
            return None
        start = max(0, maxlen - suffix_len)
        end = maxlen - 1
        return (start, end)


    if not start_str.isdigit():
        return None
    start = int(start_str)

    if end_str == "":
        end = maxlen - 1
    else:
        if not end_str.isdigit():
            return None
        end = int(end_str)

    if start > end or start >= maxlen:
        return None

    end = min(end, maxlen - 1)
    return (start, end)
