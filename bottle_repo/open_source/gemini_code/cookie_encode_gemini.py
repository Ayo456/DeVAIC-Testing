import base64
import hashlib
import hmac
import pickle

def cookie_encode(data, key: str) -> str:
    payload = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    payload_b64 = base64.urlsafe_b64encode(payload).decode("ascii")
    
    mac = hmac.new(key.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(mac).decode("ascii")
    
    return f"{sig_b64}!{payload_b64}"