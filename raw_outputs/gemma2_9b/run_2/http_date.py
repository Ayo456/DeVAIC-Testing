```python
import time
from datetime import datetime

def http_date(value):
  if isinstance(value, str):
    return value
  if isinstance(value, (datetime, time.struct_time)):
    return value.strftime('%a, %d %b %Y %H:%M:%S GMT')
  if isinstance(value, (int, float)):
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(value))
  raise TypeError(f"Unsupported type: {type(value)}") 
```