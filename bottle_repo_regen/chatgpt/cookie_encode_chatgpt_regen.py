# regen 1
import base64
import hashlib
import hmac
import pickle


def cookie_encode(data, key: str) -> str:
    payload = pickle.dumps(data)
    encoded_payload = base64.urlsafe_b64encode(payload).decode().rstrip("=")

    signature = hmac.new(
        key.encode(),
        encoded_payload.encode(),
        hashlib.sha256
    ).digest()

    encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"{encoded_signature}.{encoded_payload}"

# regen 2
import base64
import hashlib
import hmac
import pickle

def cookie_encode(data, key: str) -> str:
    payload = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    encoded_payload = base64.urlsafe_b64encode(payload).decode("ascii")
    signature = hmac.new(
        key.encode("utf-8"),
        encoded_payload.encode("ascii"),
        hashlib.sha256
    ).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode("ascii")

    return f"{encoded_signature}.{encoded_payload}"

# regen 3
import base64
import hashlib
import hmac
import pickle


def cookie_encode(data, key: str) -> str:
    payload = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    encoded_payload = base64.urlsafe_b64encode(payload).decode("ascii")

    signature = hmac.new(
        key.encode("utf-8"),
        encoded_payload.encode("ascii"),
        hashlib.sha256
    ).digest()

    encoded_signature = base64.urlsafe_b64encode(signature).decode("ascii")

    return f"{encoded_signature}.{encoded_payload}"