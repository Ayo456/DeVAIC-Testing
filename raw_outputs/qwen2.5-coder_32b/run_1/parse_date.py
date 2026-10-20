```python
from email.utils import parsedate_to_datetime
from datetime import datetime

def parse_date(ims: str) -> int:
    try:
        return int(parsedate_to_datetime(ims).timestamp())
    except (TypeError, ValueError):
        try:
            return int(datetime.strptime(ims, '%A, %d-%b-%y %H:%M:%S %Z').timestamp())
        except ValueError:
            try:
                return int(datetime.strptime(ims, '%a %b %d %H:%M:%S %Y').timestamp())
            except ValueError:
                return None
```