import re
import time
from email.utils import parsedate_tz, mktime_tz

def parse_date(ims: str):
    if not isinstance(ims, str):
        return None
    ims = ims.strip()
    t = parsedate_tz(ims)
    if t is not None:
        try:
            return float(mktime_tz(t))
        except Exception:
            return None
    m = re.match('^(.*?)(?:\\s*\\(?([A-Z]{1,4}|[+-]\\d{4})\\)?\\s*)$', ims)
    if m:
        date_part = m.group(1).strip()
        tz_part = m.group(2)
        t = parsedate_tz(date_part)
        if t is not None:
            try:
                base = mktime_tz(t)
                if tz_part and re.match('[+-]\\d{4}', tz_part):
                    sign = 1 if tz_part[0] == '+' else -1
                    hours = int(tz_part[1:3])
                    mins = int(tz_part[3:5])
                    offset = sign * (hours * 3600 + mins * 60)
                    return float(base - offset)
                return float(base)
            except Exception:
                return None
    return None