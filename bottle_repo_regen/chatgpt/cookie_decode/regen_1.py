# regen 1
import base64
import hashlib
import hmac
import pickle

def cookie_decode(data: str, key: str):
    try:
        payload, signature = data.rsplit(".", 1)

        expected_signature = hmac.new(
            key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return None

        decoded = base64.urlsafe_b64decode(payload.encode())
        return pickle.loads(decoded)

    except (ValueError, TypeError, pickle.UnpicklingError, base64.binascii.Error):
        return None
