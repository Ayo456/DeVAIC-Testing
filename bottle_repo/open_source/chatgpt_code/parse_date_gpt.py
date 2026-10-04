import calendar
from datetime import datetime


def parse_date(ims: str):
    if not isinstance(ims, str):
        return None

    formats = (
        "%a, %d %b %Y %H:%M:%S GMT",
        "%A, %d-%b-%y %H:%M:%S GMT",
        "%a %b %d %H:%M:%S %Y",
    )

    for fmt in formats:
        try:
            parsed = datetime.strptime(ims, fmt)
            return calendar.timegm(parsed.timetuple())
        except ValueError:
            pass

    return None