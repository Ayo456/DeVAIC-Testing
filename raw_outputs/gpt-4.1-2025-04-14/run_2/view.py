```python
import functools
from collections.abc import Mapping

def view(tpl_name, **defaults):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is None:
                return template(tpl_name, **defaults)
            elif isinstance(result, Mapping):
                variables = dict(defaults)
                variables.update(result)
                return template(tpl_name, **variables)
            else:
                return result
        return wrapper
    return decorator
```