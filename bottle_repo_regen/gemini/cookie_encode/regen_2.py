# regen 2
import base64
import hashlib
import hmac
import json
from typing import Any


def cookie_encode(data: Any, key: str) -> str:

    json_bytes = json.dumps(
        data, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    payload_b64 = (
        base64.urlsafe_b64encode(json_bytes).decode("utf-8").rstrip("=")
    )


    signature = hmac.new(
        key=key.encode("utf-8"),
        msg=payload_b64.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")


    return f"{sig_b64}.{payload_b64}"
