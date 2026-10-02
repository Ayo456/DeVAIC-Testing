# regen 2
def _lscmp(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a.encode("utf-8"), b.encode("utf-8")):
        result |= x ^ y
        
    return result == 0
