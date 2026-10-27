```python
import hmac
import base64
import pickle
import hashlib

def cookie_decode(data, key):
    if isinstance(data, str):
        data = data.encode('utf-8')
    if not data.startswith(b'!'):
        return None
    try:
        sig, msg = data[1:].split(b'?', 1)
    except ValueError:
        return None
    try:
        message = base64.urlsafe_b64decode(msg)
        signature = base64.urlsafe_b64decode(sig)
    except Exception:
        return None
    expected_sig = hmac.new(key.encode('utf-8'), msg, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected_sig):
        return None
    try:
        return pickle.loads(message)
    except Exception:
        return None
```