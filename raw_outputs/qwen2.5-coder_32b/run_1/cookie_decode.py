```python
import hmac
import hashlib
import pickle
import base64

def cookie_decode(data: str, key: str):
    try:
        encoded_data, signature = data.rsplit('.', 1)
        decoded_data = base64.urlsafe_b64decode(encoded_data + '==')
        expected_signature = hmac.new(key.encode(), decoded_data, hashlib.sha256).hexdigest()
        if hmac.compare_digest(signature, expected_signature):
            return pickle.loads(decoded_data)
    except (ValueError, IndexError, TypeError, pickle.UnpicklingError):
        pass
    return None
```