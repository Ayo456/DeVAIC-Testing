import re
import time
from datetime import datetime, timezone, timedelta

def parse_date(ims: str):
    rfc1123 = '^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), (\\d{2}) (\\w{3}) (\\d{4}) (\\d{2}):(\\d{2}):(\\d{2}) ([A-Za-z+-]{2,5}|\\d{4})$'
    rfc850 = '^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), (\\d{2})-(\\w{3})-(\\d{2}) (\\d{2}):(\\d{2}):(\\d{2}) ([A-Za-z+-]{2,5}|\\d{4})$'
    asctime_pat = '^(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\\w{3})\\s{1,2}(\\d{1,2}) (\\d{2}):(\\d{2}):(\\d{2}) (\\d{4})$'
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    tzmap = {'UT': 0, 'UTC': 0, 'GMT': 0, 'EST': -5 * 3600, 'EDT': -4 * 3600, 'CST': -6 * 3600, 'CDT': -5 * 3600, 'MST': -7 * 3600, 'MDT': -6 * 3600, 'PST': -8 * 3600, 'PDT': -7 * 3600}
    ims = ims.strip()
    m = re.match(rfc1123, ims)
    if m:
        day, dd, mon, yyyy, hh, mm, ss, tz = m.groups()
        try:
            dt = datetime(int(yyyy), months[mon], int(dd), int(hh), int(mm), int(ss))
        except Exception:
            return None
        if tz in tzmap:
            offset = tzmap[tz]
        elif re.match('^[+-]\\d{4}$', tz):
            sign = 1 if tz[0] == '+' else -1
            offset = sign * (int(tz[1:3]) * 3600 + int(tz[3:]) * 60)
        else:
            offset = 0
        dt = dt.replace(tzinfo=timezone(timedelta(seconds=offset)))
        return dt.timestamp()
    m = re.match(rfc850, ims)
    if m:
        day, dd, mon, yy, hh, mm, ss, tz = m.groups()
        try:
            year = int(yy)
            if year < 70:
                year += 2000
            else:
                year += 1900
            dt = datetime(year, months[mon], int(dd), int(hh), int(mm), int(ss))
        except Exception:
            return None
        if tz in tzmap:
            offset = tzmap[tz]
        elif re.match('^[+-]\\d{4}$', tz):
            sign = 1 if tz[0] == '+' else -1
            offset = sign * (int(tz[1:3]) * 3600 + int(tz[3:]) * 60)
        else:
            offset = 0
        dt = dt.replace(tzinfo=timezone(timedelta(seconds=offset)))
        return dt.timestamp()
    m = re.match(asctime_pat, ims)
    if m:
        day, mon, dd, hh, mm, ss, yyyy = m.groups()
        try:
            dt = datetime(int(yyyy), months[mon], int(dd), int(hh), int(mm), int(ss), tzinfo=timezone.utc)
        except Exception:
            return None
        return dt.timestamp()
    try:
        from email.utils import parsedate_tz, mktime_tz
        tup = parsedate_tz(ims)
        if tup is not None:
            return float(mktime_tz(tup))
    except Exception:
        pass
    return None