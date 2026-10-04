import pickle
import hmac
import hashlib
import base64

def cookie_encode(data, key: str) -> str:
    serialized_data = pickle.dumps(data)
    hmac_obj = hmac.new(key.encode(), serialized_data, hashlib.sha256)
    signature = hmac_obj.digest()
    encoded_data = base64.urlsafe_b64encode(serialized_data).rstrip(b'=')
    encoded_signature = base64.urlsafe_b64encode(signature).rstrip(b'=')
    cookie_string = f'{encoded_signature}.{encoded_data}'
    return cookie_string