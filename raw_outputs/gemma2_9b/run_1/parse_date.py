```python
from datetime import datetime

def parse_date(ims: str) -> float | None:
  try:
    dt = datetime.fromisoformat(ims).astimezone(datetime.utc)
    return dt.timestamp()
  except ValueError:
    return None
```