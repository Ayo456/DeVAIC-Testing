def view(tpl_name, **defaults):

    def decorator(func):

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, (dict,)):
                result.update(defaults)
            elif result is None:
                result = defaults
            return result if not isinstance(result, str) else template(tpl_name, **result)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator