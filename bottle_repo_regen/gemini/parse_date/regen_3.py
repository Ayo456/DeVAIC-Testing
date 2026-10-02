# regen 3
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
import calendar

def parse_date(ims: str):
    if not isinstance(ims, str):
        return None
    

    try:
        dt = parsedate_to_datetime(ims)
        if dt is not None:
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return int(dt.timestamp())
    except (TypeError, ValueError):
        pass


    try:
        dt = datetime.strptime(ims.strip(), "%a %b %d %H:%M:%S %Y")
        return calendar.timegm(dt.utctimetuple())
    except (TypeError, ValueError):
        return None
