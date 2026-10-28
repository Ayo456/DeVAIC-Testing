import time
from email.utils import parsedate_to_datetime

def parse_date(ims: str) -> float:
    try:
        dt = parsedate_to_datetime(ims)
        return dt.timestamp()
    except (TypeError, ValueError):
        return None