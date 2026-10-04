import base64
import hashlib
import hmac
import pickle
from typing import Any, Optional

def cookie_decode(data: str, key: str) -> Optional[Any]:
    if not isinstance(data, str) or not isinstance(key, str):
        return None

    parts = data.split("!", 1)
    if len(parts) != 2:
        return None

    sig_b64, payload_b64 = parts

    expected_mac = hmac.new(
        key.encode("utf-8"),
        payload_b64.encode("ascii"),
        hashlib.sha256
    ).digest()

    try:
        sig = base64.urlsafe_b64decode(sig_b64.encode("ascii"))
    except Exception:
        return None

    if not hmac.compare_digest(sig, expected_mac):
        return None

    try:
        payload = base64.urlsafe_b64decode(payload_b64.encode("ascii"))
        return pickle.loads(payload)
    except Exception:
        return None