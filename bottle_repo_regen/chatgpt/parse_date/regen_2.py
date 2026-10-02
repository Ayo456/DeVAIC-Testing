# regen 2
from datetime import datetime, timezone

def parse_date(ims: str):
    formats = [
        "%a, %d %b %Y %H:%M:%S GMT",
        "%A, %d-%b-%y %H:%M:%S GMT",
        "%a %b %d %H:%M:%S %Y"
    ]

    for fmt in formats:
        try:
            date = datetime.strptime(ims, fmt)
            date = date.replace(tzinfo=timezone.utc)
            return int(date.timestamp())
        except (ValueError, TypeError):
            continue

    return None
