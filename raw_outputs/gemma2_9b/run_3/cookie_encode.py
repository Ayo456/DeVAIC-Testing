```python
import hmac
import base64
from urllib.parse import quote

def cookie_encode(data, key: str) -> str:
  return f"{quote(base64.urlsafe_b64encode(hmac.new(key.encode(), data.encode(), 'sha256').digest()).decode())}_{quote(base64.urlsafe_b64encode(data).decode())}"
```