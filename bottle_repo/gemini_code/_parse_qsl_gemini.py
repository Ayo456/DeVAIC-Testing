from typing import List, Tuple
from urllib.parse import unquote_plus


def _parse_qsl(qs: str) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []
    if not qs or not isinstance(qs, str):
        return pairs

    for segment in qs.split("&"):
        segment = segment.strip()
        if not segment:
            continue

        if "=" in segment:
            name, value = segment.split("=", 1)
        else:
            name, value = segment, ""

        decoded_name = unquote_plus(name)
        decoded_value = unquote_plus(value)
        pairs.append((decoded_name, decoded_value))

    return pairs