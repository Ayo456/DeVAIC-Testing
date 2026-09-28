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