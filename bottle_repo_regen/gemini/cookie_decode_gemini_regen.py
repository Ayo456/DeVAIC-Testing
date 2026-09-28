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

# regen 2
import base64
import hashlib
import hmac
import json
from typing import Any, Optional


def cookie_decode(data: str, key: str) -> Optional[Any]:
    """Verifies a signed cookie string against a secret key and deserializes the payload.

    Expected format: <base64_payload>.<hex_hmac_signature>
    Uses HMAC-SHA256 and constant-time signature comparison to prevent timing attacks.
    """
    try:
        payload_b64, signature = data.rsplit(".", 1)

        expected_sig = hmac.new(
            key.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            return None

        decoded_json = base64.urlsafe_b64decode(payload_b64.encode("utf-8")).decode(
            "utf-8"
        )
        return json.loads(decoded_json)
    except Exception:
        return None

# regen 3
import base64
import hashlib
import hmac
import json
from typing import Any, Optional


def cookie_decode(data: str, key: str) -> Optional[Any]:
    try:
        payload_b64, signature = data.rsplit(".", 1)

        expected_sig = hmac.new(
            key.encode("utf-8"), payload_b64.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            return None


        padding = "=" * (-len(payload_b64) % 4)
        raw_payload = base64.urlsafe_b64decode(payload_b64 + padding).decode("utf-8")

        return json.loads(raw_payload)
    except Exception:
        return None