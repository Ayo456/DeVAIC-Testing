def _lscmp(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    result = 0
    for char_a, char_b in zip(a, b):
        result |= ord(char_a) ^ ord(char_b)
    return result == 0
print(_lscmp('hello', 'hello'))
print(_lscmp('hello', 'world'))
print(_lscmp('hello', 'hell'))