```python
from email.utils import parsedate_to_datetime
from time import mktime

def parse_date(ims: str) -> int:
    try:
        dt = parsedate_to_datetime(ims)
        return int(mktime(dt.utctimetuple()))
    except (TypeError, ValueError):
        return None
```