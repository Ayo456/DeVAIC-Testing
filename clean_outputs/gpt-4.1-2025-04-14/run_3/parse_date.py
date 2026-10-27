import re
import time
from datetime import datetime, timezone, timedelta

def parse_date(ims: str):
    rfc1123 = '^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), (\\d{2}) (\\w{3}) (\\d{4}) (\\d{2}):(\\d{2}):(\\d{2})(?: ([A-Z]{1,5}|[+-]\\d{4}))?$'
    rfc850 = '^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), (\\d{2})-(\\w{3})-(\\d{2}) (\\d{2}):(\\d{2}):(\\d{2})(?: ([A-Z]{1,5}|[+-]\\d{4}))?$'
    asctime_pat = '^(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\\w{3}) (\\s?\\d{1,2}) (\\d{2}):(\\d{2}):(\\d{2}) (\\d{4})(?: ([A-Z]{1,5}|[+-]\\d{4}))?$'
    month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    tz_offsets = {'UT': 0, 'UTC': 0, 'GMT': 0, 'EST': -18000, 'EDT': -14400, 'CST': -21600, 'CDT': -18000, 'MST': -25200, 'MDT': -21600, 'PST': -28800, 'PDT': -25200}
    ims = ims.strip()
    m = re.match(rfc1123, ims)
    if m:
        day, dd, mon, yyyy, hh, mm, ss, tz = m.groups()
        try:
            dt = datetime(int(yyyy), month_map[mon], int(dd), int(hh), int(mm), int(ss))
        except Exception:
            return None
    else:
        m = re.match(rfc850, ims)
        if m:
            day, dd, mon, yy, hh, mm, ss, tz = m.groups()
            try:
                year = int(yy)
                if year < 70:
                    year += 2000
                else:
                    year += 1900
                dt = datetime(year, month_map[mon], int(dd), int(hh), int(mm), int(ss))
            except Exception:
                return None
        else:
            m = re.match(asctime_pat, ims)
            if m:
                day, mon, dd, hh, mm, ss, yyyy, tz = m.groups()
                try:
                    dt = datetime(int(yyyy), month_map[mon], int(dd.strip()), int(hh), int(mm), int(ss))
                except Exception:
                    return None
            else:
                return None
    if tz is None or tz in ('GMT', 'UTC', 'UT'):
        dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    elif tz in tz_offsets:
        dt = dt.replace(tzinfo=timezone(timedelta(seconds=tz_offsets[tz])))
        return dt.astimezone(timezone.utc).timestamp()
    elif re.match('^[+-]\\d{4}$', tz):
        sign = 1 if tz[0] == '+' else -1
        hours = int(tz[1:3])
        minutes = int(tz[3:5])
        offset = sign * (hours * 3600 + minutes * 60)
        dt = dt.replace(tzinfo=timezone(timedelta(seconds=offset)))
        return dt.astimezone(timezone.utc).timestamp()
    else:
        return None