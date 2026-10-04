def yieldroutes(func):
    if hasattr(func, '__routes__'):
        routes = func.__routes__
        if isinstance(routes, dict):
            routes = routes.values()
        for route in routes:
            yield from yieldroutes(route)
    else:
        yield func

def route1():
    print('This is route 1')

def route2():
    print('This is route 2')

def route3():
    print('This is route 3')

class NestedRouteHandler:

    def __init__(self):
        self.__routes__ = {'route2': route2, 'route3': route3}

def standalone_route():
    print('This is a standalone route')

def main_route():
    print('This is the main route')
main_route.__routes__ = NestedRouteHandler().__routes__
for route in yieldroutes(main_route):
    print(route.__name__)