def parse_auth(header: str) -> tuple[str, str] | None:
    scheme, credentials = header.split(' ', 1) if ' ' in header else (None, None)
    if scheme.lower() == 'basic':
        try:
            user, password = base64.b64decode(credentials).decode().split(':', 1)
            return (user, password)
        except:
            return None
    return None