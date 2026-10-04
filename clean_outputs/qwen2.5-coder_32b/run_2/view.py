def template(tpl_name, **tplvars):
    return f'Template: {tpl_name} rendered with {tplvars}'

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

@view('example_template.html', title='Default Title')
def my_route_handler():
    return {'content': 'Hello, World!'}
print(my_route_handler())

@view('example_template.html', title='Default Title')
def my_route_handler_none():
    return None
print(my_route_handler_none())

@view('example_template.html', title='Default Title')
def my_route_handler_string():
    return 'This is a string response.'
print(my_route_handler_string())