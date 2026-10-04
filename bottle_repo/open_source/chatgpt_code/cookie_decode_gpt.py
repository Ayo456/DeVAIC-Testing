import base64
import binascii
import hashlib
import hmac
import pickle


def cookie_decode(data: str, key: str):
    if not isinstance(data, str) or not isinstance(key, str):
        return None

    try:
        signature, encoded = data.split(".", 1)

        expected = hmac.new(
            key.encode("utf-8"),
            encoded.encode("ascii"),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected):
            return None

        payload = base64.b64decode(
            encoded.encode("ascii"),
            altchars=b"-_",
            validate=True
        )

        return pickle.loads(payload)

    except (ValueError, UnicodeEncodeError, binascii.Error, pickle.PickleError, EOFError):
        return None