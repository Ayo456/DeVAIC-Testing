import codecs

def guess_json_utf(data):
    sample = data[:4]

    if sample in (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE):
        return "utf-32"

    if sample[:3] == codecs.BOM_UTF8:
        return "utf-8-sig"

    if sample[:2] in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE):
        return "utf-16"

    null_count = sample.count(b"\x00")

    if null_count == 0:
        return "utf-8"

    if null_count == 2:
        if sample[::2] == b"\x00\x00":
            return "utf-16-be"

        if sample[1::2] == b"\x00\x00":
            return "utf-16-le"

    if null_count == 3:
        if sample[:3] == b"\x00\x00\x00":
            return "utf-32-be"

        if sample[1:] == b"\x00\x00\x00":
            return "utf-32-le"

    return None