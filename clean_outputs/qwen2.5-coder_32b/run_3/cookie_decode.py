import hmac
import hashlib
import pickle
import base64

def cookie_decode(data: str, key: str):
    try:
        payload, sig = data.rsplit('.', 1)
        decoded_sig = base64.urlsafe_b64decode(sig + '==')
        expected_sig = hmac.new(key.encode(), payload.encode(), hashlib.sha256).digest()
        if hmac.compare_digest(decoded_sig, expected_sig):
            return pickle.loads(base64.urlsafe_b64decode(payload + '=='))
    except (ValueError, IndexError, TypeError, pickle.UnpicklingError):
        pass
    return None