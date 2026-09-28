# regen 1
def parse_range_header(header: str, maxlen: int):
    if not header or maxlen <= 0:
        return None

    if not header.startswith("bytes="):
        return None

    value = header[6:].strip()

    if "," in value or "-" not in value:
        return None

    start_str, end_str = value.split("-", 1)

    try:
        if start_str == "":
            suffix_length = int(end_str)

            if suffix_length <= 0 or suffix_length > maxlen:
                return None

            start = maxlen - suffix_length
            end = maxlen - 1

        else:
            start = int(start_str)

            if start < 0 or start >= maxlen:
                return None

            if end_str == "":
                end = maxlen - 1
            else:
                end = int(end_str)

                if end < start or end >= maxlen:
                    return None

        return (start, end)

    except ValueError:
        return None

# regen 2
def parse_range_header(header: str, maxlen: int):
    if not header or maxlen <= 0:
        return None

    if not header.startswith("bytes="):
        return None

    value = header[6:].strip()

    if "," in value or "-" not in value:
        return None

    start_str, end_str = value.split("-", 1)

    try:
        if start_str == "":
            suffix_length = int(end_str)

            if suffix_length <= 0 or suffix_length > maxlen:
                return None

            return maxlen - suffix_length, maxlen - 1

        start = int(start_str)

        if start < 0 or start >= maxlen:
            return None

        if end_str == "":
            return start, maxlen - 1

        end = int(end_str)

        if end < start or end >= maxlen:
            return None

        return start, end

    except ValueError:
        return None

# regen 3
import re

def parse_range_header(header: str, maxlen: int):
    if not isinstance(header, str) or maxlen <= 0:
        return None

    match = re.fullmatch(r"bytes=(\d*)-(\d*)", header.strip())

    if not match:
        return None

    start_str, end_str = match.groups()

    if not start_str and not end_str:
        return None

    if not start_str:
        suffix_length = int(end_str)

        if suffix_length <= 0:
            return None

        suffix_length = min(suffix_length, maxlen)
        return maxlen - suffix_length, maxlen - 1

    start = int(start_str)

    if start >= maxlen:
        return None

    if not end_str:
        return start, maxlen - 1

    end = int(end_str)

    if end < start or end >= maxlen:
        return None

    return start, end