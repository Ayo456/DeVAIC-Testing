```python
import hmac
import base64
from functools import partial

def cookie_encode(data, key: str) -> str:
  serialized_data = base64.b64encode(str(data).encode()).decode()
  signature = hmac.new(key.encode(), serialized_data.encode(), 'sha256').digest()
  return f"{serialized_data}.{base64.b64encode(signature).decode()}" 
```