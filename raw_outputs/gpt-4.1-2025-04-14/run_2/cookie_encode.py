```python
import pickle
import base64
import hmac
import hashlib

def cookie_encode(data, key):
    msg = base64.b64encode(pickle.dumps(data))
    sig = base64.b64encode(hmac.new(key.encode('utf-8'), msg, hashlib.sha256).digest())
    return b'!' + sig + b'?' + msg
```