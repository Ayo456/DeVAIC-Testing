```python
import time
from email.utils import parsedate_to_datetime

def parse_date(ims: str) -> int:
    try:
        dt = parsedate_to_datetime(ims)
        return int(dt.timestamp())
    except (TypeError, ValueError):
        return None
```