```python
import pickle
import base64
import hmac
import hashlib

def cookie_encode(data, key):
    serialized = pickle.dumps(data, protocol=4)
    message = base64.b64encode(serialized)
    signature = base64.b64encode(hmac.new(key.encode('utf-8'), message, hashlib.sha256).digest())
    return b'!' + signature + b'?' + message
```