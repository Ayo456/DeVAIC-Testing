# regen 2
from urllib.parse import unquote_plus

def _parse_qsl(qs: str) -> list[tuple[str, str]]:
    result = []

    for pair in qs.split("&"):
        if not pair:
            continue

        if "=" in pair:
            name, value = pair.split("=", 1)
        else:
            name, value = pair, ""

        name = unquote_plus(name)
        value = unquote_plus(value)

        result.append((name, value))

    return result
