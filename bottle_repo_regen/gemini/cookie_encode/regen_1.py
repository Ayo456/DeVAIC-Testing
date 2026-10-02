# regen 1
import base64
import hashlib
import hmac
import json
from typing import Any


def cookie_encode(data: Any, key: str) -> str:

    json_bytes = json.dumps(data, separators=(",", ":")).encode("utf-8")
    payload_b64 = base64.urlsafe_b64encode(json_bytes).decode("ascii").rstrip("=")


    key_bytes = key.encode("utf-8")
    signature = hmac.new(
        key_bytes, payload_b64.encode("ascii"), hashlib.sha256
    ).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")


    return f"{payload_b64}.{sig_b64}"
