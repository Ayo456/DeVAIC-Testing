import hmac
import hashlib
import pickle
import base64

def cookie_decode(data: str, key: str):
    try:
        payload, signature = data.split('.')
    except ValueError:
        return None
    try:
        payload_bytes = base64.urlsafe_b64decode(payload)
        signature_bytes = base64.urlsafe_b64decode(signature)
    except Exception:
        return None
    computed_hmac = hmac.new(key.encode(), payload_bytes, hashlib.sha256).digest()
    if not hmac.compare_digest(computed_hmac, signature_bytes):
        return None
    try:
        original_object = pickle.loads(payload_bytes)
    except Exception:
        return None
    return original_object