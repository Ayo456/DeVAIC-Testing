import datetime

def http_date(ts):
    if isinstance(ts, datetime.datetime):
        dt = ts
    else:
        dt = datetime.datetime.fromtimestamp(ts)
    return dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
timestamp = 1678886400
date_string = http_date(timestamp)
print(date_string)