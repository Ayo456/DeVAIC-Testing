from urllib.parse import unquote_plus


def _parse_qsl(qs: str):
    result = []

    for segment in qs.split("&"):
        if not segment:
            continue

        if "=" in segment:
            name, value = segment.split("=", 1)
        else:
            name, value = segment, ""

        result.append((unquote_plus(name), unquote_plus(value)))

    return result