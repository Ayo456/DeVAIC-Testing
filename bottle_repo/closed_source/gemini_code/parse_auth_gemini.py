import base64
from typing import Optional, Tuple

def parse_auth(header: str) -> Optional[Tuple[str, str]]:
    if not isinstance(header, str):
        return None

    parts = header.strip().split(None, 1)
    if len(parts) != 2:
        return None

    scheme, param = parts

    if scheme.lower() == "basic":
        try:
            decoded = base64.b64decode(param.strip()).decode("utf-8")
            if ":" not in decoded:
                return None
            user, password = decoded.split(":", 1)
            return user, password
        except Exception:
            return None

    return scheme, param