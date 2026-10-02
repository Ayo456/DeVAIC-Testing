# regen 2
import urllib.parse
from typing import List, Tuple


def _parse_qsl(qs: str) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []
    if not qs:
        return pairs


    if qs.startswith("?"):
        qs = qs[1:]


    for item in qs.replace(";", "&").split("&"):
        if not item:
            continue

        if "=" in item:
            name, value = item.split("=", 1)
        else:
            name, value = item, ""

        decoded_name = urllib.parse.unquote_plus(name)
        decoded_value = urllib.parse.unquote_plus(value)
        pairs.append((decoded_name, decoded_value))

    return pairs
