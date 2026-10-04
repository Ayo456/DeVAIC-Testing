To create a generator function `yieldroutes(func)` that inspects a route handler callback function or callable object, we need to define what "nested routes" or "wrapped child handlers" mean in this context. For the sake of this example, let's assume that a route handler might have an attribute or a method that contains nested handlers. A common pattern in web frameworks is to have a `handlers` attribute or a method like `get_handlers()` that returns a list of nested handlers.

Here's a possible implementation of the `yieldroutes` generator function:

```python
def yieldroutes(func):
    """
    Recursively yield each underlying route callback from the given function.
    If the function has nested routes or wrapped child handlers, it will yield
    each of those. Otherwise, it will yield the function itself.
    """
    # Check if the function has a 'handlers' attribute
    if hasattr(func, 'handlers'):
        for handler in func.handlers:
            yield from yieldroutes(handler)
    # Check if the function has a 'get_handlers' method
    elif hasattr(func, 'get_handlers') and callable(func.get_handlers):
        for handler in func.get_handlers():
            yield from yieldroutes(handler)
    else:
        # If no nested handlers, yield the function itself
        yield func

# Example usage:

# Define some sample route handlers
def route1():
    pass

def route2():
    pass

def route3():
    pass

# Define a class-based route handler with nested handlers
class NestedRouteHandler:
    def __init__(self):
        self.handlers = [route2, route3]

    def get_handlers(self):
        return self.handlers

# Define a class-based route handler with a 'handlers' attribute
class RouteHandlerWithHandlers:
    def __init__(self):
        self.handlers = [NestedRouteHandler()]

# Define a class-based route handler with a 'get_handlers' method
class RouteHandlerWithGetHandlers:
    def get_handlers(self):
        return [NestedRouteHandler()]

# Define a main route handler with nested handlers
def main_route_handler():
    pass

main_route_handler.handlers = [NestedRouteHandler(), RouteHandlerWithHandlers(), RouteHandlerWithGetHandlers()]

# Use the generator to yield all route handlers
for handler in yieldroutes(main_route_handler):
    print(handler.__name__ if hasattr(handler, '__name__') else handler.__class__.__name__)
```

In this example:
- `route1`, `route2`, and `route3` are simple route handlers.
- `NestedRouteHandler` is a class-based route handler with a `handlers` attribute.
- `RouteHandlerWithHandlers` is a class-based route handler with a `handlers` attribute that contains another handler.
- `RouteHandlerWithGetHandlers` is a class-based route handler with a `get_handlers` method that returns handlers.
- `main_route_handler` is a function-based route handler with nested handlers.

The `yieldroutes` function will recursively yield all the route handlers found in the nested structure.