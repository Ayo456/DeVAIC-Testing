import base64

def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    parts = header.strip().split(' ', 1)
    if len(parts) != 2:
        return None
    scheme, parameter = parts
    if scheme.lower() == 'basic':
        try:
            decoded_parameter = base64.b64decode(parameter).decode('ascii')
            user, password = decoded_parameter.split(':', 1)
            return (user, password)
        except:
            return None
    else:
        return (scheme, parameter)