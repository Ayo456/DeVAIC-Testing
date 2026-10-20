def view(tpl_name, **defaults):

    def decorator(func):

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, dict):
                tplvars = {**defaults, **result}
            elif result is None:
                tplvars = defaults
            else:
                return result
            return template(tpl_name, **tplvars)
        return wrapper
    return decorator