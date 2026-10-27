import base64
import hmac
import pickle

def cookie_decode(data, key):
    if isinstance(data, bytes):
        data = data.decode('utf-8', errors='strict')
    if not isinstance(data, str) or not data.startswith('!'):
        return None
    try:
        sig_msg = data[1:].split('?', 1)
        if len(sig_msg) != 2:
            return None
        sig_b64, msg_b64 = sig_msg
        sig = base64.urlsafe_b64decode(sig_b64 + '=' * (-len(sig_b64) % 4))
        msg_bytes = base64.urlsafe_b64decode(msg_b64 + '=' * (-len(msg_b64) % 4))
        expected_sig = hmac.new(key.encode('utf-8'), msg_b64.encode('utf-8'), 'sha256').digest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        return pickle.loads(msg_bytes)
    except Exception:
        return None