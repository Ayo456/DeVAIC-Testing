import base64

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    parts = header.split(' ')
    if len(parts) != 2:
        return None
    scheme, parameter = parts
    if scheme.lower() == 'basic':
        try:
            decoded_payload = base64.b64decode(parameter).decode('utf-8')
            user, password = decoded_payload.split(':', 1)
            return (user, password)
        except:
            return None
    else:
        return (scheme, parameter)