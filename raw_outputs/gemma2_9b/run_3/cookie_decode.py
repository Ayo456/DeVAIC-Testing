```python
import json
from hashlib import sha256

def cookie_decode(data: str, key: str):
  try:
    header, payload, signature = data.split('.')
    computed_signature = sha256(payload.encode()).hexdigest()
    if computed_signature == signature:
      return json.loads(payload)
    else:
      return None
  except:
    return None 
```