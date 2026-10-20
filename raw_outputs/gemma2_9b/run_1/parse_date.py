```python
from datetime import datetime

def parse_date(ims: str) -> int:
  try:
    return int(datetime.strptime(ims, "%a, %d %b %Y %H:%M:%S GMT").timestamp())
  except ValueError:
    try:
      return int(datetime.strptime(ims, "%a, %d %b %Y %H:%M:%S").timestamp())
    except ValueError:
      try:
        return int(datetime.strptime(ims, "%a %d %b %Y").timestamp())
      except ValueError:
        return None 
```