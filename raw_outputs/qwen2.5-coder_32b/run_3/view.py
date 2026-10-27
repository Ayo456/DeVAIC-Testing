```python
import functools

def view(tpl_name, **defaults):
    def decorator(handler):
        @functools.wraps(handler)
        def wrapper(*args, **kwargs):
            result = handler(*args, **kwargs)
            if isinstance(result, dict):
                variables = {**defaults, **result}
            elif result is None:
                variables = defaults
            else:
                return result
            return template(tpl_name, **variables)
        return wrapper
    return decorator
```