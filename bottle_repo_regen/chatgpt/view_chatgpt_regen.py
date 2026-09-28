# regen 1
from functools import wraps

def view(tpl_name, **defaults):
    def decorator(callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)

            if result is None:
                return template(tpl_name, **defaults)

            if isinstance(result, dict):
                tplvars = defaults.copy()
                tplvars.update(result)
                return template(tpl_name, **tplvars)

            return result

        return wrapper

    return decorator

# regen 2
from functools import wraps

def view(tpl_name, **defaults):
    def decorator(callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)

            if result is None:
                return template(tpl_name, **defaults)

            if isinstance(result, dict):
                tplvars = defaults.copy()
                tplvars.update(result)
                return template(tpl_name, **tplvars)

            return result

        return wrapper

    return decorator

# regen 3
def view(tpl_name, **defaults):
    def decorator(callback):
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)

            if isinstance(result, dict):
                tplvars = defaults.copy()
                tplvars.update(result)
                return template(tpl_name, **tplvars)

            if result is None:
                return template(tpl_name, **defaults)

            return result

        return wrapper

    return decorator