import base64
import hmac
import hashlib
import pickle

def cookie_decode(data: str, key: str) -> object:
    parts = data.split('.')
    if len(parts) != 2:
        return None
    encoded_payload, signature = parts
    try:
        payload = base64.urlsafe_b64decode(encoded_payload + '==')
    except Exception:
        return None
    expected_signature = hmac.new(key.encode(), payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        return None
    try:
        obj = pickle.loads(payload)
    except Exception:
        return None
    return obj