def parse_auth(header: str) -> tuple:
    if not isinstance(header, str):
        return None
    parts = header.split()
    if len(parts) != 2:
        return None
    scheme, parameter = parts
    if scheme.lower() == 'basic':
        try:
            decoded = base64.b64decode(parameter).decode('ascii')
            user, password = decoded.split(':', 1)
            return (user, password)
        except:
            return None
    return (scheme, parameter)