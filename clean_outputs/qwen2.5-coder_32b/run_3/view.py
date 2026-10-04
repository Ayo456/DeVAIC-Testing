from functools import wraps

def view(tpl_name, **defaults):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
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
    return f'Rendering {tpl_name} with variables: {tplvars}'

@view('example_template.html', default_key='default_value')
def example_route():
    return {'custom_key': 'custom_value'}
print(example_route())