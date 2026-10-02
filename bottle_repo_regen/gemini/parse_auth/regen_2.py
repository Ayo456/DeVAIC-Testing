# regen 2
import base64
from typing import Optional, Tuple


def parse_auth(header: str) -> Optional[Tuple[str, str]]:
    if not isinstance(header, str):
        return None


    parts = header.strip().split(None, 1)
    if len(parts) != 2:
        return None

    scheme, param = parts[0], parts[1].strip()
    if not scheme or not param:
        return None

    if scheme.lower() == "basic":
        try:
            decoded = base64.b64decode(param, validate=True).decode("utf-8")
        except Exception:
            return None

        if ":" not in decoded:
            return None

        username, password = decoded.split(":", 1)
        return (username, password)

    return (scheme, param)
