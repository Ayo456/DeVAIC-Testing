def view(tpl_name, **defaults):

    def decorator(callback):

        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)
            if isinstance(result, dict):
                return template(tpl_name, **{**defaults, **result})
            elif result is None:
                return template(tpl_name, **defaults)
            return result
        return wrapper
    return decorator