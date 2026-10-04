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