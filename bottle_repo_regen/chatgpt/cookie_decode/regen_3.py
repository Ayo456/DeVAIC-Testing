# regen 3
import base64
import hashlib
import hmac
import pickle

def cookie_decode(data: str, key: str):
    try:
        if not data.startswith("!") or "?" not in data:
            return None

        signature, payload = data[1:].split("?", 1)

        expected = hmac.new(
            key.encode(),
            payload.encode(),
            hashlib.sha256
        ).digest()

        expected_signature = base64.b64encode(expected).decode()

        if not hmac.compare_digest(signature, expected_signature):
            return None

        decoded = base64.b64decode(payload)
        return pickle.loads(decoded)

    except (ValueError, TypeError, pickle.UnpicklingError, base64.binascii.Error):
        return None
