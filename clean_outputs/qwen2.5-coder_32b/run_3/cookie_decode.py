import base64
import hmac
import hashlib
import json

def cookie_decode(data: str, key: str):
    try:
        decoded_data = base64.urlsafe_b64decode(data)
    except Exception:
        return None
    try:
        payload, signature = decoded_data.rsplit(b'.', 1)
    except ValueError:
        return None
    try:
        hmac_obj = hmac.new(key.encode(), payload, hashlib.sha256)
        expected_signature = hmac_obj.digest()
    except Exception:
        return None
    if not hmac.compare_digest(signature, expected_signature):
        return None
    try:
        original_object = json.loads(payload.decode())
    except Exception:
        return None
    return original_object