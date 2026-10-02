# regen 3
from datetime import datetime, timezone
from typing import Optional


def parse_date(ims: str) -> Optional[int]:
    formats = [
        "%a, %d %b %Y %H:%M:%S GMT",
        "%A, %d-%b-%y %H:%M:%S GMT",
        "%a %b %d %H:%M:%S %Y"
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(ims, fmt)
            dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
        except (ValueError, TypeError):
            continue

    return None
