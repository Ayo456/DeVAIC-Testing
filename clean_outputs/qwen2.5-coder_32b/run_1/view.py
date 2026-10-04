from functools import wraps

def view(tpl_name, **defaults):

    def decorator(callback):

        @wraps(callback)
        def wrapper(*args, **kwargs):
            result = callback(*args, **kwargs)
            if isinstance(result, dict):
                tplvars = {**defaults, **result}
            elif result is None:
                tplvars = defaults
            else:
                return result
            return template(tpl_name, **tplvars)
        return wrapper
    return decorator

def template(tpl_name, **tplvars):
    return f'Template {tpl_name} rendered with {tplvars}'

@view('example_template.html', default_key='default_value')
def example_handler():
    return {'handler_key': 'handler_value'}
print(example_handler())