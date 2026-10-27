```python
import base64
from hashlib import hmac

def cookie_decode(data, key):
  if isinstance(data, str):
    data = data.encode()
  parts = data.split(b'?', 1)
  if len(parts) != 2:
    return None
  message = parts[1]
  signature = parts[0]
  try:
    decoded_message = base64.b64decode(message)
  except:
    return None
  computed_signature = hmac(key.encode(), message, digestmod='sha256').digest()
  try:
    decoded_signature = base64.b64decode(signature)
  except:
    return None
  return None if hmac(key.encode(), decoded_message, digestmod='sha256').digest() != decoded_signature else eval(decoded_message.decode()) 
```