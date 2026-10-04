def _lscmp(a: str, b: str) -> bool:
    result = 0
    for i in range(min(len(a), len(b))):
        result |= ord(a[i]) ^ ord(b[i])
    return result == 0 and len(a) == len(b)