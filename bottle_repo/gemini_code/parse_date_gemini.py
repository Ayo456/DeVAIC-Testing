import calendar
import email.utils
from typing import Optional

def parse_date(ims: str) -> Optional[int]:
    if not isinstance(ims, str):
        return None

    try:
        parsed = email.utils.parsedate(ims.strip())
        if parsed is None:
            return None
        return int(calendar.timegm(parsed))
    except Exception:
        return None