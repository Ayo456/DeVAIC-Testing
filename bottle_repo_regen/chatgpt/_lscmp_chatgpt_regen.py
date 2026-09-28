# regen 1
import hmac

def _lscmp(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)

# regen 2
import hmac

def _lscmp(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))

# regen 3
import hmac

def _lscmp(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))