import hmac
import base64
from urllib.parse import urlencode

def cookie_encode(data, key: str) -> str:
    serialized_data = base64.b64encode(str(data).encode()).decode()
    signature = hmac.new(key.encode(), serialized_data.encode(), 'sha256').digest()
    signature_base64 = base64.b64encode(signature).decode()
    cookie_data = {'data': serialized_data, 'signature': signature_base64}
    return urlencode(cookie_data)