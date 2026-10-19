import hmac


def _lscmp(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)