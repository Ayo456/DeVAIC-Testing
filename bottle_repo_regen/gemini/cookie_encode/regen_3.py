# regen 3
import base64
import hashlib
import hmac
import json
from typing import Any


def cookie_encode(data: Any, key: str) -> str:
    """Serializes data to JSON, signs it with HMAC-SHA256, and returns a URL-safe string."""
    payload_bytes = json.dumps(data, separators=(",", ":")).encode("utf-8")
    payload_b64 = (
        base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
    )

    signature = hmac.new(
        key.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256
    ).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")

    return f"{sig_b64}.{payload_b64}"
