# regen 3
from urllib.parse import unquote_plus

def _parse_qsl(qs: str):
    result = []

    for part in qs.split("&"):
        if not part:
            continue

        if "=" in part:
            name, value = part.split("=", 1)
        else:
            name, value = part, ""

        name = unquote_plus(name)
        value = unquote_plus(value)

        result.append((name, value))

    return result
