import hmac
import base64
import pickle

def cookie_decode(data, key):
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    if not data.startswith('!') or '?' not in data:
        return None
    sig, msg = data[1:].split('?', 1)
    try:
        expected_sig = base64.b64encode(hmac.new(key.encode(), msg.encode(), 'sha256').digest()).decode('utf-8')
        if not hmac.compare_digest(sig, expected_sig):
            return None
        return pickle.loads(base64.b64decode(msg))
    except (ValueError, pickle.UnpicklingError):
        return None