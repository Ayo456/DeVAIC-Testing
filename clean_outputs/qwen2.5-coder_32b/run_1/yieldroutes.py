def yieldroutes(func):
    if hasattr(func, '__child_routes__'):
        for child in func.__child_routes__:
            yield from yieldroutes(child)
    else:
        yield func

def standalone_route():
    return 'Standalone route'

def parent_route():
    return 'Parent route'
parent_route.__child_routes__ = [standalone_route, lambda: 'Child route 1', lambda: 'Child route 2']
for route in yieldroutes(parent_route):
    print(route.__name__ if hasattr(route, '__name__') else route.__class__.__name__)