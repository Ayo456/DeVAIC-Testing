```python
import hmac
import base64
import pickle

def cookie_decode(data, key):
    if isinstance(data, str):
        data = data.encode('utf-8')
    if not data.startswith(b'!'):
        return None
    try:
        sig_end = data.index(b'?', 1)
        signature = data[1:sig_end]
        message = data[sig_end + 1:]
        expected_signature = base64.b64encode(hmac.new(key.encode('utf-8'), message, 'sha256').digest())
        if not hmac.compare_digest(signature, expected_signature):
            return None
        return pickle.loads(base64.b64decode(message))
    except (ValueError, IndexError, pickle.UnpicklingError):
        return None
```