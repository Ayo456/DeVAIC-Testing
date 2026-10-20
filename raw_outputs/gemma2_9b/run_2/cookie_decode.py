```python
import json
from hashlib import sha256

def cookie_decode(data: str, key: str) -> object:
  try:
    signature, payload = data.split('.')
    decoded_payload = json.loads(base64.b64decode(payload))
    computed_signature = sha256(payload.encode()).hexdigest()
    if computed_signature == signature:
      return decoded_payload
    else:
      return None
  except:
    return None 
```