```python
import re
import time
from email.utils import parsedate_tz, mktime_tz

def parse_date(ims: str):
    if not isinstance(ims, str):
        return None
    ims = ims.strip()
    # Try email.utils.parsedate_tz (handles RFC 1123, RFC 850, asctime, and timezones)
    t = parsedate_tz(ims)
    if t is not None:
        try:
            return float(mktime_tz(t))
        except Exception:
            return None
    # Try to parse timezone offset manually if present (e.g., "Sun, 06 Nov 1994 08:49:37 GMT+0200")
    # Regex to extract date and offset
    m = re.match(r'^(.*?)(?:\s*\(?([A-Z]{1,4}|[+-]\d{4})\)?\s*)$', ims)
    if m:
        date_part = m.group(1).strip()
        tz_part = m.group(2)
        t = parsedate_tz(date_part)
        if t is not None:
            try:
                base = mktime_tz(t)
                # If tz_part is a numeric offset like +0200 or -0700
                if tz_part and re.match(r'[+-]\d{4}', tz_part):
                    sign = 1 if tz_part[0] == '+' else -1
                    hours = int(tz_part[1:3])
                    mins = int(tz_part[3:5])
                    offset = sign * (hours * 3600 + mins * 60)
                    # mktime_tz assumes UTC if no offset, so adjust
                    return float(base - offset)
                # If tz_part is a known abbreviation, ignore (already handled by parsedate_tz)
                return float(base)
            except Exception:
                return None
    return None
```