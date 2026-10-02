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
