# regen 3
import base64
from typing import Optional, Tuple


def parse_auth(header: str) -> Optional[Tuple[str, str]]:
    if not isinstance(header, str):
        return None

    header = header.strip()
    if not header:
        return None

    parts = header.split(maxsplit=1)
    if len(parts) != 2:
        return None

    scheme, param = parts

    if scheme.lower() == "basic":
        try:
            decoded = base64.b64decode(param, validate=True).decode("utf-8")
        except Exception:
            return None

        if ":" not in decoded:
            return None

        user, password = decoded.split(":", 1)
        return (user, password)

    return (scheme, param)
