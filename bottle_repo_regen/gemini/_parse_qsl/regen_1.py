# regen 1
import urllib.parse


def _parse_qsl(qs: str) -> list[tuple[str, str]]:
    result = []
    for segment in qs.split("&"):
        if not segment:
            continue
        if "=" in segment:
            name, value = segment.split("=", 1)
        else:
            name, value = segment, ""
        name = urllib.parse.unquote_plus(name)
        value = urllib.parse.unquote_plus(value)
        result.append((name, value))
    return result
