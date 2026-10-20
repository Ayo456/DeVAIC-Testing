```python
import hmac
import hashlib
import base64
import pickle

def cookie_encode(data, key: str) -> str:
    serialized_data = pickle.dumps(data)
    signature = hmac.new(key.encode(), serialized_data, hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=').decode()
    encoded_data = base64.urlsafe_b64encode(serialized_data).rstrip(b'=').decode()
    return f"{encoded_signature}.{encoded_data}"
```