# regen 1
import base64
import hashlib
import hmac
import json
from typing import Any, Optional


def cookie_decode(data: str, key: str) -> Optional[Any]:
    try:
        payload_b64, signature = data.rsplit(".", 1)
        expected_sig = hmac.new(
            key.encode("utf-8"),
            payload_b64.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(expected_sig, signature):
            return None

        decoded_json = base64.urlsafe_b64decode(payload_b64.encode("utf-8")).decode(
            "utf-8"
        )
        return json.loads(decoded_json)
    except Exception:
        return None
