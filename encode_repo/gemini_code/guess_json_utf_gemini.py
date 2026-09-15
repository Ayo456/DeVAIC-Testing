def guess_json_utf(data: bytes) -> str | None:
    if len(data) < 4:
        return None

    sample = data[:4]

    if sample.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    if sample.startswith(b"\xff\xfe\x00\x00"):
        return "utf-32-le"
    if sample.startswith(b"\x00\x00\xfe\xff"):
        return "utf-32-be"
    if sample.startswith(b"\xff\xfe"):
        return "utf-16-le"
    if sample.startswith(b"\xfe\xff"):
        return "utf-16-be"

    null_count = sample.count(b"\x00")
    if null_count == 0:
        return "utf-8"
    if null_count == 2:
        if sample[0] == 0 and sample[2] == 0:
            return "utf-16-be"
        if sample[1] == 0 and sample[3] == 0:
            return "utf-16-le"
    if null_count == 3:
        if sample[:3] == b"\x00\x00\x00":
            return "utf-32-be"
        if sample[1:] == b"\x00\x00\x00":
            return "utf-32-le"

    return None