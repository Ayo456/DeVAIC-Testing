def _lscmp(a, b):
    if type(a) != type(b):
        raise TypeError('Both arguments must be of the same type')
    if not (isinstance(a, (str, bytes)) and isinstance(b, (str, bytes))):
        raise TypeError('Arguments must be str or bytes')
    if len(a) != len(b):
        return False
    result = 0
    if isinstance(a, str):
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
    else:
        for x, y in zip(a, b):
            result |= x ^ y
    return result == 0