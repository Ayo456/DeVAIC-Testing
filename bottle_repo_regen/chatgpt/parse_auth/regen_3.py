# regen 3
import base64


def parse_auth(header: str):
    if not isinstance(header, str):
        return None

    try:
        scheme, parameter = header.strip().split(None, 1)

        if scheme.lower() == "basic":
            decoded = base64.b64decode(parameter).decode("utf-8")

            if ":" not in decoded:
                return None

            user, password = decoded.split(":", 1)
            return user, password

        return scheme, parameter

    except (ValueError, TypeError, UnicodeDecodeError, base64.binascii.Error):
        return None
