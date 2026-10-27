import base64
import hmac
import pickle

def cookie_decode(data, key):
    if isinstance(data, str):
        data = data.encode('utf-8')
    if not data.startswith(b'!'):
        return None
    try:
        sig_msg = data[1:].split(b'?', 1)
        if len(sig_msg) != 2:
            return None
        sig_b64, msg_b64 = sig_msg
        sig = base64.urlsafe_b64decode(sig_b64 + b'=' * (-len(sig_b64) % 4))
        msg = msg_b64
        expected_sig = hmac.new(key.encode('utf-8'), msg, 'sha256').digest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        obj_bytes = base64.urlsafe_b64decode(msg + b'=' * (-len(msg) % 4))
        return pickle.loads(obj_bytes)
    except Exception:
        return None