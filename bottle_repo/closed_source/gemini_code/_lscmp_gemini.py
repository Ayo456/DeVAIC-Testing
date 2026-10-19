def _lscmp(a: str, b: str) -> bool:
    if not isinstance(a, str) or not isinstance(b, str):
        return False

    a_bytes = a.encode("utf-8")
    b_bytes = b.encode("utf-8")

    result = len(a_bytes) ^ len(b_bytes)
    for x, y in zip(a_bytes, b_bytes):
        result |= x ^ y

    return result == 0