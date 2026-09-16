import base64
import hashlib
import hmac
import pickle


def cookie_encode(data, key: str) -> str:
    payload = pickle.dumps(data)
    encoded = base64.urlsafe_b64encode(payload).decode("ascii")
    signature = hmac.new(
        key.encode("utf-8"),
        encoded.encode("ascii"),
        hashlib.sha256
    ).hexdigest()

    return f"{signature}.{encoded}"