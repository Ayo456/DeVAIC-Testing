# regen 1
from urllib.parse import unquote_plus

def _parse_qsl(qs: str) -> list[tuple[str, str]]:
    result = []

    for segment in qs.split("&"):
        if not segment:
            continue

        if "=" in segment:
            name, value = segment.split("=", 1)
        else:
            name, value = segment, ""

        name = unquote_plus(name)
        value = unquote_plus(value)

        result.append((name, value))

    return result
