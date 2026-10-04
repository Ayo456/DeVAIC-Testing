def yieldroutes(func):
    if hasattr(func, 'handlers'):
        for handler in func.handlers:
            yield from yieldroutes(handler)
    elif hasattr(func, 'get_handlers') and callable(func.get_handlers):
        for handler in func.get_handlers():
            yield from yieldroutes(handler)
    else:
        yield func

def route1():
    pass

def route2():
    pass

def route3():
    pass

class NestedRouteHandler:

    def __init__(self):
        self.handlers = [route2, route3]

    def get_handlers(self):
        return self.handlers

class RouteHandlerWithHandlers:

    def __init__(self):
        self.handlers = [NestedRouteHandler()]

class RouteHandlerWithGetHandlers:

    def get_handlers(self):
        return [NestedRouteHandler()]

def main_route_handler():
    pass
main_route_handler.handlers = [NestedRouteHandler(), RouteHandlerWithHandlers(), RouteHandlerWithGetHandlers()]
for handler in yieldroutes(main_route_handler):
    print(handler.__name__ if hasattr(handler, '__name__') else handler.__class__.__name__)