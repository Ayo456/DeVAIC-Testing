import base64
import binascii


def parse_auth(header: str):
    if not isinstance(header, str):
        return None

    parts = header.strip().split(None, 1)

    if len(parts) != 2:
        return None

    scheme, parameter = parts

    if scheme.lower() != "basic":
        return scheme, parameter

    try:
        decoded = base64.b64decode(parameter, validate=True).decode("utf-8")

        if ":" not in decoded:
            return None

        user, password = decoded.split(":", 1)
        return user, password

    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None