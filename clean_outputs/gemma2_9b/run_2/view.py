from functools import wraps

def template(tpl_name, **tplvars):
    raise NotImplementedError('Please implement your template rendering function')

def view(tpl_name, **defaults):

    def decorator(callback):

        @wraps(callback)
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)
            if isinstance(result, dict):
                result.update(defaults)
                return template(tpl_name, **result)
            elif result is None:
                return template(tpl_name, **defaults)
            else:
                return result
        return wrapper
    return decorator