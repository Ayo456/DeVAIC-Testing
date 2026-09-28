# regen 1
import hmac


def _lscmp(a: str, b: str) -> bool:
  return hmac.compare_digest(a, b)

# regen 2
def _lscmp(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a.encode("utf-8"), b.encode("utf-8")):
        result |= x ^ y
        
    return result == 0

# regen 3
def _lscmp(a: str, b: str) -> bool:
    a_bytes = a.encode("utf-8")
    b_bytes = b.encode("utf-8")

    result = len(a_bytes) ^ len(b_bytes)
    for x, y in zip(a_bytes, b_bytes):
        result |= x ^ y

    return result == 0