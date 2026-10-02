# regen 2
import base64
import hashlib
import hmac
import pickle


def cookie_decode(data: str, key: str):
    try:
        if not data.startswith("!") or "?" not in data:
            return None

        signature, payload = data[1:].split("?", 1)

        payload_bytes = payload.encode("ascii")
        key_bytes = key.encode("utf-8")

        expected = hmac.new(
            key_bytes,
            payload_bytes,
            digestmod=hashlib.sha256
        ).digest()

        expected_signature = base64.b64encode(expected).decode("ascii")

        if not hmac.compare_digest(signature, expected_signature):
            return None

        return pickle.loads(base64.b64decode(payload_bytes))
    except (ValueError, TypeError, UnicodeEncodeError, pickle.PickleError):
        return None
