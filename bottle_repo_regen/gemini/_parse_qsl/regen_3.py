# regen 3
from urllib.parse import unquote_plus


def _parse_qsl(qs: str) -> list[tuple[str, str]]:
    pairs = []

    for segment in qs.replace(";", "&").split("&"):
        if not segment:
            continue

        if "=" in segment:
            name, value = segment.split("=", 1)
        else:
            name, value = segment, ""

        name = unquote_plus(name)
        value = unquote_plus(value)
        pairs.append((name, value))

    return pairs
