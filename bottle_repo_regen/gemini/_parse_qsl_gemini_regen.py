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