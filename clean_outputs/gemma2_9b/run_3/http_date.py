from datetime import datetime

def http_date(ts):
    return datetime.utcfromtimestamp(ts).strftime('%a, %d %b %Y %H:%M:%S GMT')