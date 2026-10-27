```python
import pickle
import base64
import hmac
import hashlib

def cookie_encode(data, key):
    message = base64.b64encode(pickle.dumps(data))
    signature = base64.b64encode(hmac.new(key.encode(), message, hashlib.sha256).digest())
    return b'!' + signature + b'?' + message
```