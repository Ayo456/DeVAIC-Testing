import base64

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    try:
        parts = header.split(' ', 1)
        if len(parts) != 2:
            return None
        scheme, parameter = parts
        if scheme.lower() == 'basic':
            try:
                decoded_bytes = base64.b64decode(parameter)
                decoded_str = decoded_bytes.decode('utf-8')
                user, password = decoded_str.split(':', 1)
                return (user, password)
            except (base64.binascii.Error, UnicodeDecodeError, ValueError):
                return None
        else:
            return (scheme, parameter)
    except Exception:
        return None