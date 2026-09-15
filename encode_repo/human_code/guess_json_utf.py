import typing


def guess_json_utf(data: bytes) -> typing.Optional[str]:
    sample = data[:4]
    if sample in (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE):
        return "utf-32"  
    if sample[:3] == codecs.BOM_UTF8:
        return "utf-8-sig"  
    if sample[:2] in (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE):
        return "utf-16"  
    nullcount = sample.count(_null)
    if nullcount == 0:
        return "utf-8"
    if nullcount == 2:
        if sample[::2] == _null2: 
            return "utf-16-be"
        if sample[1::2] == _null2: 
            return "utf-16-le"
    if nullcount == 3:
        if sample[:3] == _null3:
            return "utf-32-be"
        if sample[1:] == _null3:
            return "utf-32-le"
    return None