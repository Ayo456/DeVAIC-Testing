# regen 3
def _lscmp(a: str, b: str) -> bool:
    a_bytes = a.encode("utf-8")
    b_bytes = b.encode("utf-8")

    result = len(a_bytes) ^ len(b_bytes)
    for x, y in zip(a_bytes, b_bytes):
        result |= x ^ y

    return result == 0
