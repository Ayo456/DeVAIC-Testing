import hmac
import base64
from urllib.parse import quote

def cookie_encode(data, key: str) -> str:
    serialized_data = base64.b64encode(str(data).encode()).decode()
    signature = hmac.new(key.encode(), serialized_data.encode(), 'sha256').digest().hex()
    cookie_string = f'signature={quote(signature)}; payload={quote(serialized_data)}'
    return cookie_string